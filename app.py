
import sys
import os
import logging
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from thompson_sampling.bernoulli import BernoulliExperiment
from thompson_sampling.priors import BetaPrior
from flasgger import Swagger
from flasgger.utils import swag_from

# Configure logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
Swagger(app)

# Basic authentication
def check_auth(username, password):
    user = "user"
    pw_hash = generate_password_hash("password")
    return username == user and check_password_hash(pw_hash, password)

def authenticate():
    return jsonify({"error": "Authentication required"}), 401

def requires_auth(f):
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return wrapped

@app.route('/update', methods=['POST'])
@swag_from('swagger.yaml', endpoint='update')
@requires_auth
def update():
    request_data = None
    if request.content_type == 'application/json':
        request_data = request.get_json()

    try:
        if request_data is None:
            return jsonify({"error": "Invalid content type"}), 400

        update_arm = request_data['update_arm']
        reward = request_data['reward']

        prior = BetaPrior()
        prior.add_one(mean=update_arm['mean'], variance=update_arm['variance'], effective_size=update_arm['effective_size'], label=update_arm['label'])

        experiment = BernoulliExperiment(priors=prior)
        experiment.add_rewards([{"label": update_arm['label'], "reward": reward}])

        new_arm = [{"label": arm.label, "mean": arm.mean, "variance": arm.variance, "effective_size": arm.effective_size} for arm in experiment.arms]
        return jsonify({"arm": new_arm})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/choose', methods=['POST'])
@swag_from('swagger.yaml', endpoint='choose')
@requires_auth
def choose():
    request_data = None
    if request.content_type == 'application/json':
        request_data = request.get_json()

    try:
        if request_data is None:
            return jsonify({"error": "Invalid content type"}), 400

        arms = request_data['arms']

        # Validate data
        if not validate_arms(arms):
            return jsonify({"error": "Invalid arm data"}), 400

        priors = BetaPrior()
        for arm in arms:
            priors.add_one(mean=arm['mean'], variance=arm['variance'], effective_size=arm['effective_size'], label=arm['label'])

        experiment = BernoulliExperiment(priors=priors)
        chosen_arm = experiment.choose_arm()
        return jsonify({"chosen_arm": chosen_arm})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def log_request(response):
    if response.content_length and response.content_length > 0:
        logger.info(f"Request Method: {request.method}, Request Path: {request.path}, Response Status: {response.status}")
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

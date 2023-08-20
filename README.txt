
Thompson Sampling Multi-Armed Bandit Microservice
=================================================

This microservice provides a Thompson Sampling approach to a Multi-Armed Bandit problem. It offers two main endpoints for updating arm information and choosing an arm.

API Endpoints
-------------

1. **Update Arm Information** (`POST /update`)
   - Description: Updates the information of a given arm and returns the new arm information.
   - Request Body:
     - `update_arm`: The arm to update (mean, variance, effective size, label).
     - `reward`: The reward for the arm being updated.
   - Example Request:
     ```json
     {
       "update_arm": {"mean": 0.5, "variance": 0.2, "effective_size": 10, "label": "option1"},
       "reward": 1
     }
     ```
   - Response: Updated arm information.
   - Example Response:
     ```json
     {"arm": [{"label": "option1", "mean": 0.51, "variance": 0.19, "effective_size": 11}]}
     ```

2. **Choose an Arm** (`POST /choose`)
   - Description: Takes all the arms and their information, then chooses an arm and returns it.
   - Request Body:
     - `arms`: List of arms with their information (mean, variance, effective size, label).
   - Example Request:
     ```json
     {"arms": [{"mean": 0.5, "variance": 0.2, "effective_size": 10, "label": "option1"}]}
     ```
   - Response: Chosen arm label.
   - Example Response:
     ```json
     {"chosen_arm": "option1"}
     ```

API Documentation
-----------------

API documentation is available through Swagger UI at `/apidocs/index.html` on the running service.

Authentication
--------------

Authentication is required for both endpoints:
- Default Username: `user`
- Default Password: `password`
- Authentication Method: HTTP Basic Authentication

Logging
-------

Logging is implemented using the Python logging module. Logs are directed to stderr.

Installation on Cloud Run
-------------------------

1. Build the Docker image:
   ```
   docker build -t thompson-sampling .
   ```

2. Push the image to a container registry:
   ```
   docker push thompson-sampling
   ```

3. Deploy to Cloud Run:
   ```
   gcloud run deploy --image thompson-sampling --platform managed
   ```

Understanding Thompson Sampling
-------------------------------

Thompson Sampling is a probabilistic algorithm used for solving the Multi-Armed Bandit problem. In this problem, you have multiple options (arms), each with an unknown reward probability. The goal is to find the arm with the highest expected reward over a series of trials.

- **Mean**: The average reward for an arm. It represents the probability of success for that arm.
- **Variance**: A measure of how much the rewards vary for an arm. A higher variance means more uncertainty.
- **Effective Size**: The number of trials that contributed to the mean and variance. A higher effective size means more confidence in the mean and variance.
- **Label**: A unique identifier for each arm.

Thompson Sampling uses these parameters to model the uncertainty about the true reward probabilities and balances exploration (trying new arms) with exploitation (choosing the best-known arm).

For more detailed information, please refer to scholarly articles and textbooks on Thompson Sampling and Multi-Armed Bandits.

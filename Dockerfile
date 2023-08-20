
# Use a base image with both Rust and Python
FROM rust:1-slim as rust-base

# Install Python
RUN apt-get update -y && apt-get install -y python3 python3-pip

# Create a work directory
WORKDIR /app

# Copy app.py and swagger.yaml
COPY app.py ./
COPY swagger.yaml ./

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Install thompson-sampling from source
RUN pip3 install thompson-sampling

# Expose port 8080
EXPOSE 8080

# Run app.py using gunicorn with a timeout of 2400 seconds
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--timeout", "2400", "app:app"]

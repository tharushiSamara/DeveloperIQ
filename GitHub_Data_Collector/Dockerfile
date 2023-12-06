# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /github_data_collector


COPY GitHub_Data_Collector/ .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV SERVICE_NAME=GitHub_Data_Collector

# Run app.py when the container launches
CMD ["python", "github_data_collector.py"]


# docker build -f ./GitHub_Data_Collector/Dockerfile -t github-data-collector:v1 .
#docker tag 2b5cca3b1495 tharushisamara/developer-test:latest
# docker run tharushisamara/developer-test  --- to test your Docker image locally.
# docker tag github_data_collector:v1 tharushisamara/developer-test:v1
# docker login
# docker push tharushisamara/developer-test:latest

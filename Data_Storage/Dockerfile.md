# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /data_storage


COPY Data_Storage/ .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5003

# Define environment variable
ENV SERVICE_NAME=Data_Storage

# Run app.py when the container launches
CMD ["python", "data_storage.py"]


# docker build -t ./Data_Storage/data-storage:v1 .
# 2. Run docker ps and get the tagID
# docker tag <tagID> tharushisamara/developer-test:v1
# docker login
# docker push tharushisamara/developer-test:latest

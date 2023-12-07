# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /data_processor


COPY Data_Processor/ .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5002

# Define environment variable
ENV SERVICE_NAME=Data_Processor

# Run app.py when the container launches
CMD ["python", "data_processor.py"]


# docker build -f ./Data_Processor/Dockerfile -t data_processor:v1 .
# docker tag data_processor:v1 tharushisamara/data_processor:v1
# docker login
# docker push tharushisamara/developer-test:latest

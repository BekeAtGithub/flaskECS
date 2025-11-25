# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container 
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV HOSTNAME Node

# Run app.py when the container launches
CMD ["python", "app.py"]

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

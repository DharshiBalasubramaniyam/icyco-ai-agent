# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user with UID 10014 (required by Checkov)
RUN addgroup -S appgroup && adduser -S -u 10014 appuser -G appgroup

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set non-root user (UID 10014)
USER 10014

# Expose the port Flask runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask app
CMD ["flask", "run"]

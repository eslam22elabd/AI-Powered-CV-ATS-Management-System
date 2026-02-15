# Dockerfile

# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first for better caching
COPY src/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
# This copies everything from src/ to /app
COPY src/ .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python","0.0.0.0:5000","main:app"]

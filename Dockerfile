# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Tesseract OCR and other dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y poppler-utils && \
    apt-get install -y libnss3 && \
    apt-get clean

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the application runs on
EXPOSE 4000

# Run the application
CMD ["python", "app.py"]

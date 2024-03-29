FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y poppler-utils && \
    apt-get install -y libnss3 && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the application runs on
EXPOSE 4000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4000"]

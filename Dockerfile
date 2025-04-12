# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the app and templates
COPY app.py .
COPY requirements.txt .
COPY templates ./templates

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]

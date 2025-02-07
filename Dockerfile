# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1

# Command to run Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_default_superuser && python manage.py runserver 0.0.0.0:8000"]
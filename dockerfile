# Dockerfile
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE pricing_api.settings

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations
RUN python manage.py migrate

# Create superuser (non-interactive) - remove in production or pass variables securely
RUN python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Load initial data
#CMD python manage.py loaddata initial_data.json

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["daphne", "pricing_api.asgi:application", "--port", "8000", "--bind", "0.0.0.0"]


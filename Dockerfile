# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables to avoid writing .pyc files and to buffer outputs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app code to container
COPY . /app/

# Collect static files (if you have static files)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "restaurant_booking.wsgi:application", "--bind", "0.0.0.0:8000"]

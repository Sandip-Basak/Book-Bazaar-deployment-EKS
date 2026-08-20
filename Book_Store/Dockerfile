FROM python:3.11-slim

# Install system dependencies for mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Start the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Book_Store.wsgi:application"]

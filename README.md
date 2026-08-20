# Online Book Store - AWS EKS Deployment

This repository contains a simple Django application for an online book store. It has been updated to connect to an AWS RDS MySQL instance and uses AWS S3 for hosting both static assets and user-uploaded media (book photos).

The goal is to deploy the application's infrastructure on AWS EKS using Terraform and deploy the application itself using a Helm Chart.

## Features
- **Django Application**: Book store backend with admin panel support.
- **AWS S3 Integration**: Automatically uploads user media (like book photos) and serves static files using AWS S3 via `django-storages`.
- **AWS RDS MySQL Integration**: Configured to connect to AWS RDS instances using environment variables.
- **Dockerized**: Includes a Dockerfile and docker-compose.yml to easily test the application locally with a MySQL container.

## Current Progress
- [x] Application updated to upload media and static files to AWS S3.
- [x] Settings updated to connect to MySQL (AWS RDS ready).
- [x] `requirements.txt` generated with all dependencies (`django-storages`, `boto3`, `mysqlclient`, etc.).
- [x] `Dockerfile` and `docker-compose.yml` created for local development and containerization.
- [ ] Terraform code for infrastructure (EKS, RDS, S3).
- [ ] Helm Chart for deploying the application.

## Prerequisites
- Docker and Docker Compose (for local testing)
- AWS Account with S3 Bucket and RDS instance (for production/deployment)
- AWS Credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)

## Local Development (Docker Compose)

You can run the application locally using Docker Compose, which will spin up the Django web server and a local MySQL database. 

1. Ensure Docker is running.
2. In the `Book_Store` directory, create a `.env` file (or provide environment variables directly) if you want to use S3 locally, or just run the compose file:
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   export AWS_STORAGE_BUCKET_NAME="your_bucket_name"
   ```
3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
4. Access the application at `http://localhost:8000`.

*Note: For the application to fully work with the database, you will need to run migrations inside the container:*
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Environment Variables

The application relies on the following environment variables for configuration:

### Database (MySQL/RDS)
- `DB_NAME`: Database name (default: `online_store`)
- `DB_USER`: Database user (default: `root`)
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (e.g., your RDS endpoint)
- `DB_PORT`: Database port (default: `3306`)

### AWS S3
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: Name of your S3 bucket
- `AWS_S3_REGION_NAME`: AWS region of the bucket (default: `us-east-1`)

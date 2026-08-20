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
- [x] Terraform code for infrastructure (EKS, RDS, S3).
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

## Infrastructure Deployment (Terraform)

The `terraform/` directory contains all the Infrastructure as Code (IaC) to provision the required resources on AWS.

### Resources Provisioned:
- **VPC**: A dedicated VPC with 2 public and 2 private subnets across 2 Availability Zones, including a NAT Gateway.
- **EKS Cluster**: An Amazon EKS cluster (v1.35) with a managed node group consisting of `t3.medium` instances.
- **RDS MySQL**: A secure MySQL 8.0 instance (`db.t3.micro`) inside the private subnets.
- **S3 Bucket**: A private bucket for storing media and static files, uniquely named with a random suffix.
- **IRSA (IAM Roles for Service Accounts)**: Configures a Kubernetes Service Account (`book-store-sa`) with permissions to access the S3 bucket securely, eliminating the need to pass AWS access keys to the application pods.

### How to Deploy

Ensure you have [Terraform](https://developer.hashicorp.com/terraform/downloads) installed and your AWS CLI is authenticated with sufficient permissions.

1. **Navigate to the Terraform directory:**
   ```bash
   cd terraform
   ```

2. **Initialize Terraform:**
   This will download the necessary AWS and Kubernetes provider plugins and modules.
   ```bash
   terraform init
   ```

3. **Plan the Deployment:**
   Review the resources that Terraform will create.
   ```bash
   terraform plan
   ```

4. **Apply the Changes:**
   Execute the deployment. This process will take around 15-20 minutes, primarily for the EKS cluster and RDS instance to spin up.
   ```bash
   terraform apply
   ```
   *Type `yes` when prompted to confirm.*

5. **Retrieve Outputs:**
   Once completed, Terraform will output essential information required for the next steps (like the database endpoint, generated password, and S3 bucket name). You can always retrieve these values by running:
   ```bash
   terraform output
   ```

6. **Connect to the EKS Cluster:**
   Update your local `kubeconfig` to interact with your new cluster using `kubectl`:
   ```bash
   aws eks update-kubeconfig --region us-east-1 --name book-bazaar-cluster
   ```

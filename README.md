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
- [x] Helm Chart for deploying the application.

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
- `CLOUDFRONT_DOMAIN`: (Optional) The CloudFront distribution domain name (e.g., `d1234abcd.cloudfront.net`). If provided, media and static files will be served via the CDN globally.

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

## Application Deployment (Helm)

The `book-bazaar-chart/` directory contains a Helm chart to deploy the Django application to your EKS cluster. It seamlessly integrates with the AWS resources created by Terraform.

### Chart Components:
- **Deployment**: Runs your Django application (default 2 replicas).
- **ServiceAccount**: Configured to match the `book-store-sa` IRSA role for passwordless S3 access.
- **Secret**: Securely passes your database credentials and AWS configuration to the pods as environment variables using base64 encoding.
- **Service**: A `LoadBalancer` service exposing your application on port 80 to the internet.

### How to Deploy

Ensure your `kubeconfig` is pointing to your EKS cluster (Step 6 of Terraform deployment).

1. **Build and Push your Docker Image:**
   You need to build the Docker image and push it to your AWS ECR repository.
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and push
   docker build -t book-bazaar .
   docker tag book-bazaar:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/book-bazaar:latest
   docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/book-bazaar:latest
   ```

2. **Update `values.yaml`:**
   Open `book-bazaar-chart/values.yaml` and update the `env:` and `image:` sections with the outputs from Terraform and your ECR registry:
   ```yaml
   image:
     repository: "YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/book-bazaar"

   serviceAccount:
     annotations:
       eks.amazonaws.com/role-arn: "YOUR_IRSA_ROLE_ARN"

   env:
     dbPassword: "BookBazaarSecurePass123!"
     dbHost: "YOUR_DB_ENDPOINT"
     awsStorageBucketName: "YOUR_S3_BUCKET_NAME"
     cloudfrontDomain: "YOUR_CLOUDFRONT_DOMAIN"
   ```

3. **Install the Helm Chart:**
   Navigate back to the root directory and run:
   ```bash
   helm install book-bazaar ./book-bazaar-chart
   ```

4. **Verify Deployment & Get URL:**
   ```bash
   # Check if pods are running
   kubectl get pods
   
   # Get the LoadBalancer URL to access the application
   kubectl get svc book-bazaar
   ```

## Operational Commands (Kubernetes)

Once your application is deployed to EKS, you may need to perform some operational tasks.

### Running Database Migrations
When deploying for the first time (or after changing your Django models), you must run migrations to set up the database tables in RDS:
```bash
kubectl exec -it $(kubectl get pods -l app.kubernetes.io/name=book-bazaar -o jsonpath='{.items[0].metadata.name}') -- python manage.py migrate
```

### Uploading Static Files (CSS/JS) to S3
When you deploy the application, you need to collect and upload Django's static files (including the admin panel styles) to your S3 bucket. Run this command to automatically upload them:
```bash
kubectl exec -it $(kubectl get pods -l app.kubernetes.io/name=book-bazaar -o jsonpath='{.items[0].metadata.name}') -- python manage.py collectstatic --noinput
```

### Creating an Admin Superuser (Interactive)
To access the Django admin panel, you need an admin account. You can create a superuser interactively by running:
```bash
kubectl exec -it $(kubectl get pods -l app.kubernetes.io/name=book-bazaar -o jsonpath='{.items[0].metadata.name}') -- python manage.py createsuperuser
```
*Note: The `-it` flags are required here because `createsuperuser` prompts you for input (username, email, password).*

### Running Arbitrary Commands (Bash Shell)
If you ever need to inspect the container from the inside, you can open an interactive bash shell in the running pod:
```bash
kubectl exec -it $(kubectl get pods -l app.kubernetes.io/name=book-bazaar -o jsonpath='{.items[0].metadata.name}') -- /bin/bash
```

### Viewing Application Logs
If you need to debug errors (like a 500 Internal Server Error) or view standard output, you can stream logs from your pods:
```bash
kubectl logs -l app.kubernetes.io/name=book-bazaar
```

### Restarting the Application
If you pushed a new Docker image with the `latest` tag and need to force the cluster to pull it and restart the pods:
```bash
kubectl rollout restart deployment book-bazaar
```

### Upgrading the Helm Chart
If you made changes to `values.yaml` or any template files in the `book-bazaar-chart/` directory, apply the changes without downtime:
```bash
helm upgrade book-bazaar ./book-bazaar-chart
```

## Clean Up / Teardown (Avoid AWS Charges!)

To destroy all the infrastructure and avoid ongoing AWS charges, you must follow these steps in exact order. 

**1. Delete the Kubernetes Application & Load Balancer**
Because the Load Balancer was created by Kubernetes (not Terraform directly), you must delete the Helm chart first so Kubernetes can clean it up:
```bash
helm uninstall book-bazaar
```

**2. Empty the S3 Bucket**
Terraform cannot delete an S3 bucket if it still contains files. You must empty it using the AWS CLI (replace the bucket name with your actual bucket name):
```bash
aws s3 rm s3://YOUR_S3_BUCKET_NAME --recursive
```

**3. Destroy the Infrastructure**
Finally, navigate to the `terraform` directory and destroy all resources (VPC, EKS, RDS, S3, CloudFront):
```bash
cd terraform
terraform destroy
```
*Type `yes` when prompted to confirm. This will take about 15 minutes to fully tear down.*

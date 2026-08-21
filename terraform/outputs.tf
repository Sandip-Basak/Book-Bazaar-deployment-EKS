output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "rds_endpoint" {
  description = "RDS connection endpoint"
  value       = module.db.db_instance_endpoint
}

output "rds_username" {
  description = "RDS master username"
  value       = module.db.db_instance_username
}

output "rds_password" {
  description = "RDS master password"
  value       = random_password.db_password.result
  sensitive   = true
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = module.s3_bucket.s3_bucket_id
}

output "irsa_role_arn" {
  description = "IAM Role ARN for the EKS Service Account"
  value       = module.iam_eks_role.iam_role_arn
}

output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.s3_distribution.domain_name
}

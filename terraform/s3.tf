resource "random_string" "s3_suffix" {
  length  = 8
  special = false
  upper   = false
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket = "${var.project_name}-media-${random_string.s3_suffix.result}"
  acl    = "private"

  # Block public access as access will be via IRSA / Presigned URLs / IAM
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning = {
    enabled = true
  }
}

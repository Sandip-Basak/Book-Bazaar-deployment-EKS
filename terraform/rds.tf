resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

module "db_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS MySQL"
  vpc_id      = module.vpc.vpc_id

  # Ingress from EKS Nodes
  ingress_with_source_security_group_id = [
    {
      from_port                = 3306
      to_port                  = 3306
      protocol                 = "tcp"
      description              = "MySQL access from EKS nodes"
      source_security_group_id = module.eks.node_security_group_id
    }
  ]
}

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.project_name}-db"

  engine               = "mysql"
  engine_version       = "8.0"
  family               = "mysql8.0" # DB parameter group
  major_engine_version = "8.0"      # DB option group
  instance_class       = "db.t3.micro"

  allocated_storage = 20

  db_name                     = "online_store"
  username                    = "admin"
  password                    = random_password.db_password.result
  manage_master_user_password = false

  vpc_security_group_ids = [module.db_security_group.security_group_id]
  subnet_ids             = module.vpc.private_subnets
  create_db_subnet_group = true

  # Disable backups and deletion protection for simple testing/dev setup
  backup_retention_period = 0
  deletion_protection     = false
  skip_final_snapshot     = true
}

provider "aws" {
  region = var.aws_region
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = var.secret_arn
}

locals {
  secret_data = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)
}

resource "aws_docdb_cluster" "default" {
  cluster_identifier = var.cluster_id
  engine             = "docdb"
  master_username    = local.secret_data[var.secret_username_key]
  master_password    = local.secret_data[var.secret_password_key]

  backup_retention_period = 0
  skip_final_snapshot     = true
}

resource "aws_docdb_cluster_instance" "default" {
  identifier          = "${var.cluster_id}-instance-1"
  cluster_identifier  = aws_docdb_cluster.default.id
  instance_class      = var.instance_class
  engine              = "docdb"
  engine_version      = "4.0.0"
  apply_immediately   = true
}

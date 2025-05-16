provider "aws" {
  region = var.aws_region
}

resource "aws_docdb_subnet_group" "docdb_subnet_group" {
  name       = "docdb-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "DocDB Subnet Group"
  }
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = var.secret_arn
}

locals {
  secret_data = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)
}

resource "aws_docdb_cluster" "main" {
  cluster_identifier = var.db_cluster_identifier
  engine             = "docdb"
  master_username    = local.secret_data[var.secret_username_key]
  master_password    = local.secret_data[var.secret_password_key]
  db_subnet_group_name         = aws_docdb_subnet_group.docdb_subnet_group.name
  vpc_security_group_ids       = var.vpc_security_group_ids
  skip_final_snapshot          = true
  backup_retention_period      = 0
  deletion_protection          = false
  apply_immediately            = true

  tags = {
    Name = "MainDocDBCluster"
  }
}

resource "aws_docdb_cluster_instance" "main_instance" {
  identifier         = "${var.db_cluster_identifier}-instance"
  cluster_identifier = aws_docdb_cluster.main.id
  instance_class     = var.db_instance_class
  apply_immediately  = true

  tags = {
    Name = "MainDocDBInstance"
  }
}
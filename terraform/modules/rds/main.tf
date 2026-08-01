resource "aws_security_group" "database" {
  name_prefix = "${var.name}-rds-"
  description = "PostgreSQL access from the EKS VPC"
  vpc_id      = var.vpc_id
  ingress {
    description = "PostgreSQL from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  tags = merge(var.tags, { Name = "${var.name}-rds" })
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-rds"
  subnet_ids = var.private_subnet_ids
  tags       = var.tags
}

resource "aws_db_instance" "this" {
  identifier                   = "${var.name}-postgres"
  engine                       = "postgres"
  engine_version               = var.engine_version
  instance_class               = var.instance_class
  allocated_storage            = var.allocated_storage
  max_allocated_storage        = var.max_allocated_storage
  storage_encrypted            = true
  db_name                      = var.database_name
  username                     = var.master_username
  password                     = var.master_password
  port                         = 5432
  multi_az                     = var.multi_az
  backup_retention_period      = var.backup_retention_days
  deletion_protection          = var.deletion_protection
  skip_final_snapshot          = !var.deletion_protection
  publicly_accessible          = false
  db_subnet_group_name         = aws_db_subnet_group.this.name
  vpc_security_group_ids       = [aws_security_group.database.id]
  performance_insights_enabled = var.performance_insights_enabled
  tags                         = var.tags
}

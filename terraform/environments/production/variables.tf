variable "aws_region" { type = string }
variable "cluster_name" { type = string }
variable "github_repository" { type = string }
variable "media_bucket_name" { type = string }
variable "rds_master_password" { type = string }
variable "vpc_cidr" { type = string }
variable "cluster_version" { type = string }
variable "node_instance_types" { type = list(string) }

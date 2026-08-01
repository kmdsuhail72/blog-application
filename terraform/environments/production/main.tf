terraform {
  required_version = ">= 1.6.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {}
}

provider "aws" { region = var.aws_region }

module "platform" {
  source                           = "../../modules/platform"
  name                             = "blog-production"
  cluster_name                     = var.cluster_name
  github_repository                = var.github_repository
  media_bucket_name                = var.media_bucket_name
  rds_master_password              = var.rds_master_password
  vpc_cidr                         = var.vpc_cidr
  cluster_version                  = var.cluster_version
  node_instance_types              = var.node_instance_types
  node_desired_size                = 3
  node_min_size                    = 3
  node_max_size                    = 6
  rds_instance_class               = "db.t4g.medium"
  rds_multi_az                     = true
  rds_deletion_protection          = true
  rds_performance_insights_enabled = true
  tags                             = { Project = "blog-platform", Environment = "production", ManagedBy = "terraform" }
}

output "cluster_name" { value = module.platform.cluster_name }
output "github_actions_role_arn" { value = module.platform.github_actions_role_arn }
output "ecr_repository_urls" { value = module.platform.ecr_repository_urls }
output "rds_endpoint" { value = module.platform.rds_endpoint }

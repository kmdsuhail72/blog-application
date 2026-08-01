terraform {
  required_version = ">= 1.6.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {}
}

provider "aws" { region = var.aws_region }

module "platform" {
  source                           = "../../modules/platform"
  name                             = "blog-staging"
  cluster_name                     = var.cluster_name
  github_repository                = var.github_repository
  media_bucket_name                = var.media_bucket_name
  rds_master_password              = var.rds_master_password
  vpc_cidr                         = "10.15.0.0/16"
  nat_gateway_per_az               = true
  node_instance_types              = ["t3.medium"]
  node_desired_size                = 2
  node_min_size                    = 2
  node_max_size                    = 4
  rds_instance_class               = "db.t4g.small"
  rds_multi_az                     = false
  rds_deletion_protection          = true
  rds_performance_insights_enabled = true
  tags                             = { Project = "blog-platform", Environment = "staging", ManagedBy = "terraform" }
}

output "cluster_name" { value = module.platform.cluster_name }
output "github_actions_role_arn" { value = module.platform.github_actions_role_arn }

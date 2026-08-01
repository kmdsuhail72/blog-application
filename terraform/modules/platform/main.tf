resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = []
  tags            = var.tags
}

module "vpc" {
  source             = "../vpc"
  name               = var.name
  cluster_name       = var.cluster_name
  vpc_cidr           = var.vpc_cidr
  nat_gateway_per_az = var.nat_gateway_per_az
  tags               = var.tags
}

module "iam" {
  source                   = "../iam"
  name                     = var.name
  github_oidc_provider_arn = aws_iam_openid_connect_provider.github.arn
  github_repository        = var.github_repository
  tags                     = var.tags
}

module "eks" {
  source                  = "../eks"
  name                    = var.name
  cluster_name            = var.cluster_name
  cluster_version         = var.cluster_version
  vpc_id                  = module.vpc.vpc_id
  private_subnet_ids      = module.vpc.private_subnet_ids
  cluster_role_arn        = module.iam.cluster_role_arn
  node_role_arn           = module.iam.node_role_arn
  github_actions_role_arn = module.iam.github_actions_role_arn
  instance_types          = var.node_instance_types
  desired_size            = var.node_desired_size
  min_size                = var.node_min_size
  max_size                = var.node_max_size
  tags                    = var.tags
}

module "ecr" {
  source       = "../ecr"
  repositories = ["blog-backend", "blog-frontend"]
  tags         = var.tags
}

module "media" {
  source      = "../s3"
  bucket_name = var.media_bucket_name
  tags        = var.tags
}

module "rds" {
  source                       = "../rds"
  name                         = var.name
  vpc_id                       = module.vpc.vpc_id
  vpc_cidr                     = var.vpc_cidr
  private_subnet_ids           = module.vpc.private_subnet_ids
  master_password              = var.rds_master_password
  instance_class               = var.rds_instance_class
  multi_az                     = var.rds_multi_az
  deletion_protection          = var.rds_deletion_protection
  performance_insights_enabled = var.rds_performance_insights_enabled
  tags                         = var.tags
}

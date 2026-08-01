output "cluster_name" { value = module.eks.cluster_name }
output "cluster_endpoint" { value = module.eks.cluster_endpoint }
output "github_actions_role_arn" { value = module.iam.github_actions_role_arn }
output "ecr_repository_urls" { value = module.ecr.repository_urls }
output "media_bucket_name" { value = module.media.bucket_name }
output "rds_endpoint" { value = module.rds.endpoint }

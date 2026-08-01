output "cluster_role_arn" { value = aws_iam_role.cluster.arn }
output "node_role_arn" { value = aws_iam_role.node.arn }
output "github_actions_role_arn" { value = try(aws_iam_role.github_actions[0].arn, null) }

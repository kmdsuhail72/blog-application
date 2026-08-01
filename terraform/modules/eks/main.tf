resource "aws_security_group" "cluster" {
  name_prefix = "${var.name}-eks-cluster-"
  description = "Additional security group for the EKS control plane"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name}-eks-cluster" })
}

resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = var.cluster_role_arn
  version  = var.cluster_version

  vpc_config {
    subnet_ids              = var.private_subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.endpoint_public_access
    security_group_ids      = [aws_security_group.cluster.id]
  }

  access_config { authentication_mode = "API_AND_CONFIG_MAP" }
  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  tags                      = var.tags
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.name}-managed"
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.private_subnet_ids
  instance_types  = var.instance_types
  capacity_type   = "ON_DEMAND"

  scaling_config {
    desired_size = var.desired_size
    min_size     = var.min_size
    max_size     = var.max_size
  }
  update_config { max_unavailable_percentage = 33 }
  tags = var.tags
}

resource "aws_eks_addon" "this" {
  for_each                    = toset(["vpc-cni", "coredns", "kube-proxy", "metrics-server"])
  cluster_name                = aws_eks_cluster.this.name
  addon_name                  = each.value
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"
  depends_on                  = [aws_eks_node_group.this]
}

resource "aws_eks_access_entry" "github_actions" {
  count         = var.github_actions_role_arn == null ? 0 : 1
  cluster_name  = aws_eks_cluster.this.name
  principal_arn = var.github_actions_role_arn
  type          = "STANDARD"
}

resource "aws_eks_access_policy_association" "github_actions_admin" {
  count         = var.github_actions_role_arn == null ? 0 : 1
  cluster_name  = aws_eks_cluster.this.name
  principal_arn = var.github_actions_role_arn
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
  access_scope { type = "cluster" }
  depends_on = [aws_eks_access_entry.github_actions]
}

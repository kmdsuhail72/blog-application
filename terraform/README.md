# AWS infrastructure

Terraform provisions independent dev, staging, and production stacks. Each stack includes an isolated VPC, EKS managed node group, ECR repositories, encrypted S3 media bucket, private PostgreSQL RDS instance, and a GitHub Actions OIDC role.

## Bootstrap remote state

Create the shared state backend before initializing an environment:

    cd terraform/bootstrap
    terraform init
    terraform apply -var="aws_region=ap-south-1" -var="state_bucket_name=YOUR_UNIQUE_STATE_BUCKET"

Copy a target environment's backend.hcl.example to backend.hcl, replace the bucket and region, and keep it local.

## Provision an environment

    cd terraform/environments/production
    copy terraform.tfvars.example terraform.tfvars
    terraform init -backend-config=backend.hcl
    terraform plan
    terraform apply

Set TF_VAR_rds_master_password in the shell or CI secret store. Do not save production passwords in tfvars files. Use Terraform outputs to configure the EKS cluster name, ECR repositories, and GitHub Actions role in GitHub secrets.

## Configure Kubernetes

    aws eks update-kubeconfig --name blog-production --region ap-south-1
    kubectl apply -f ../../k8s/platform/namespaces.yaml

Install ingress-nginx and cert-manager using k8s/platform/README.md. Then deploy the Helm chart to production with ingress enabled and the intended DNS name.

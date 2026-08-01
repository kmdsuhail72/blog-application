# CI/CD pipeline

GitHub Actions validates pull requests and deploys successful pushes to `main`.

## Workflows

| Workflow | Trigger | Responsibility |
| --- | --- | --- |
| `backend-ci.yml` | Backend changes on pull requests and `main` | Ruff, Black, pytest, and Docker build validation |
| `frontend-ci.yml` | Frontend changes on pull requests and `main` | ESLint, production build, optional test script, and Docker build validation |
| `docker-build.yml` | Pull requests, `main`, manual | Builds both images, scans with Trivy, and publishes `SHA`, `main`, and `latest` tags after a `main` push |
| `gitops-promote.yml` | Successful image publishing workflow, manual | Commits the immutable production image SHA; Argo CD reconciles the resulting desired state |

Argo CD applies the Helm release from Git with automated sync, pruning, and self-healing. Promotion is serialized, and rollback is performed by reverting the GitOps promotion commit.

## Required GitHub configuration

Create a GitHub Environment named `production` and require reviewers as appropriate. Add these repository or environment secrets:

| Secret | Purpose |
| --- | --- |
| `AWS_GITHUB_ACTIONS_ROLE_ARN` | IAM role assumed through GitHub OIDC |
| `AWS_REGION` | AWS region containing ECR and EKS |
| `AWS_ACCOUNT_ID` | AWS account ID used to construct the ECR registry URL |
| `ECR_BACKEND_REPOSITORY` | Backend ECR repository name, such as `blog-backend` |
| `ECR_FRONTEND_REPOSITORY` | Frontend ECR repository name, such as `blog-frontend` |
| `SLACK_WEBHOOK_URL` | Optional Slack incoming webhook for deploy and rollback status |

The OIDC role needs permission to publish to ECR. Argo CD and External Secrets Operator access the cluster and runtime secrets; EKS worker nodes need permission to pull from the two ECR repositories.

## Release operations

Push application changes to `main` to create immutable image tags equal to the commit SHA. The promotion workflow records that exact SHA in `gitops/environments/production/values.yaml`, which Argo CD reconciles. To promote an existing image manually, run **Promote Production GitOps Release** and enter its SHA.

To recover from an operational issue, revert the promotion commit that introduced the image SHA. Argo CD detects the Git change and restores the prior desired release.

Protect `main` by requiring the Backend CI, Frontend CI, and Build, Scan, and Publish Images checks before merging.

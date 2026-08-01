# GitOps with Argo CD

Argo CD owns application reconciliation. CI publishes immutable images, then commits the desired production image SHA to gitops/environments/production/values.yaml. Do not use kubectl or Helm directly to modify managed application resources.

## One-time bootstrap

Install Argo CD and apply the project and applications:

    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    kubectl apply -f gitops/bootstrap

Replace every REPLACE_WITH value before applying the bootstrap. The Argo CD project deliberately allows only the dev, staging, and production namespaces.

Install External Secrets Operator with its maintained Helm chart, configure its service account with an IAM role able to read the named AWS Secrets Manager paths, then apply the store and environment ExternalSecret:

    kubectl apply -f gitops/external-secrets/cluster-secret-store.yaml
    kubectl apply -f gitops/external-secrets/production.yaml

Install the Argo Rollouts controller before enabling the production canary configuration:

    kubectl create namespace argo-rollouts
    kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

Production enables a backend canary rollout with pauses at 10%, 30%, and 60%. To roll back, revert the GitOps promotion commit or abort the rollout in Argo Rollouts, then make the desired state explicit in Git.

## Operations

Use kubectl get applications -n argocd to view sync and health status. Argo CD auto-syncs, self-heals drift, and prunes resources removed from Git. To access the UI locally, port-forward argocd-server on port 8080 and retrieve the initial password from argocd-initial-admin-secret.

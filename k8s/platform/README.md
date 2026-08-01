# EKS platform add-ons

Apply namespaces after connecting kubectl to the cluster:

    kubectl apply -f namespaces.yaml

Install ingress-nginx and cert-manager using their maintained Helm charts. Pin the chart versions after testing them in staging:

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
    helm repo add jetstack https://charts.jetstack.io
    helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set crds.enabled=true

Replace the email in cluster-issuer.yaml before applying it:

    kubectl apply -f cluster-issuer.yaml

The EKS Terraform module installs the managed metrics-server add-on. Verify metrics with kubectl top nodes. The Helm application chart provides resource requests, limits, HPA, ingress, and an application network policy.

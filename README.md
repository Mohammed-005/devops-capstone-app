# DevOps Capstone Project

This repository contains the application code and infrastructure manifests for an end-to-end CI/CD pipeline. The project demonstrates containerization, automated vulnerability scanning, cloud registry integration, and GitOps-based deployment.

## Architecture & Pipeline Flow

The project uses a pull-based GitOps model to manage deployments:

1. **Continuous Integration (GitHub Actions):** 
   - Triggers on pushes to the `main` branch.
   - Builds a Docker image and tags it with the Git commit SHA.
   - Runs a Trivy vulnerability scan against the image.
   - Pushes the verified artifact to a private AWS ECR registry.

2. **Continuous Deployment (ArgoCD & Kubernetes):** 
   - ArgoCD runs inside the cluster and monitors the `k8s/` directory.
   - When manifests are updated, ArgoCD automatically syncs the state of the cluster to match Git.
   - Kubernetes pulls the new image from AWS ECR using an image pull secret.
   - Updates are handled via rolling deployments to ensure zero downtime.

3. **Observability:** 
   - The cluster is instrumented with Prometheus and Grafana to scrape metrics and monitor application health endpoints.

## Technology Stack

* **Application:** Python, Flask, Gunicorn
* **Containerization:** Docker (distroless/slim base images)
* **Orchestration:** Kubernetes (KinD)
* **CI/CD:** GitHub Actions, ArgoCD 
* **Security:** Aqua Trivy
* **Cloud Infrastructure:** AWS Elastic Container Registry (ECR)

## Repository Structure

├── .github/workflows/ci.yaml # CI pipeline definition
├── k8s/                      # Kubernetes manifests
│   ├── app-deploy.yaml       # Deployment configuration (2 replicas)
│   └── ingress.yaml          # NGINX Ingress routing
├── Dockerfile                # Multi-stage image build steps
├── argocd-app.yaml           # ArgoCD Application manifest
├── app.py                    # Flask microservice
└── requirements.txt          # App dependencies

## Technical Notes

* **Security:** The Docker container is configured to run as a non-root user (`appuser`). AWS credentials are managed securely via GitHub Secrets.
* **GitOps Approach:** Using ArgoCD prevents the need to expose the Kubernetes API to external CI servers, significantly reducing the attack surface.
# DevOps Capstone Project

This repository contains the application code and infrastructure manifests for an end-to-end CI/CD pipeline. The project demonstrates containerization, automated vulnerability scanning, cloud registry integration, dynamic Helm templating, and GitOps-based deployment with autoscaling.

## Architecture & Pipeline Flow

The project uses a pull-based GitOps model to manage deployments:

1. **Continuous Integration (GitHub Actions):** 
   - Triggers on pushes to the `main` branch.
   - Builds a Docker image and tags it with the Git commit SHA.
   - Runs a Trivy vulnerability scan against the image.
   - Pushes the verified artifact to a private AWS ECR registry.

2. **Continuous Deployment (ArgoCD & Kubernetes):** 
   - ArgoCD runs inside the cluster and monitors the `helm/capstone-chart/` directory.
   - When templates or `values.yaml` are updated, ArgoCD automatically renders the Helm chart and syncs the state of the cluster to match Git.
   - Kubernetes pulls the new image from AWS ECR using an image pull secret.
   - Updates are handled via rolling deployments to ensure zero downtime.

3. **Auto-Scaling (HPA & Metrics Server):**
   - The cluster is configured with Kubernetes Metrics Server.
   - A Horizontal Pod Autoscaler (HPA) monitors pod CPU usage against defined limits and requests.
   - Automatically scales application replicas up under heavy load and scales down to conserve cluster resources.

4. **Observability:** 
   - The cluster is instrumented with Prometheus and Grafana to scrape metrics and monitor application health endpoints.

## Technology Stack

* **Application:** Python, Flask, Gunicorn
* **Containerization:** Docker (distroless/slim base images)
* **Orchestration:** Kubernetes (KinD)
* **Packaging & Templating:** Helm
* **CI/CD:** GitHub Actions, ArgoCD 
* **Security:** Aqua Trivy
* **Cloud Infrastructure:** AWS Elastic Container Registry (ECR)

## Repository Structure

```text
├── .github/workflows/ci.yaml # CI pipeline definition
├── helm/capstone-chart/      # Helm chart for application infrastructure
│   ├── Chart.yaml            # Chart metadata and versioning
│   ├── values.yaml           # Configuration variables (replicas, image tags, targets)
│   └── templates/            # Dynamic K8s manifests (deployment, service, hpa)
├── Dockerfile                # Multi-stage image build steps
├── argocd-app.yaml           # ArgoCD Application manifest pointing to Helm path
├── app.py                    # Flask microservice
└── requirements.txt          # App dependencies
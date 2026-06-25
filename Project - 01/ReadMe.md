# DevOps Project 01 — Simple Flask App

<img width="980" height="167" alt="image" src="https://github.com/user-attachments/assets/063918fd-0eb4-486c-b0cd-595a3617f31f" />


![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5?style=flat&logo=kubernetes&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)

> A minimalist Python Flask application wired into a complete **CI / Continuous Delivery** pipeline.  
> The focus of this project is the **infrastructure and tooling** around the app — not the app itself.

---

## What This Project Is (and Isn't)

This project demonstrates a **CI / Continuous Delivery** setup, *not* full Continuous Deployment.

| Term | What it means here |
|---|---|
| **CI (Continuous Integration)** | Every `git push` to `main` automatically triggers GitHub Actions — it lints the code, builds a Docker image, and pushes it to Docker Hub. Fully automated. |
| **Continuous Delivery** | The built image is *ready* to deploy at any time. But the actual deployment to the Minikube cluster is performed **manually** via `kubectl` commands. This mirrors real-world workflows where production deployments require human review and approval before going live. |

> **⚠️ Scope of this version:**  
> Monitoring (Prometheus + Grafana) and Chaos Engineering scenarios are **not included** in this version.  
> These are planned for a future iteration of the project.

---

## Architecture

```
  LOCAL DEV                 CI PIPELINE                  REGISTRY            MANUAL DEPLOY
  ─────────────────         ────────────────────         ─────────────       ─────────────────────
                            Triggered on every
  Write Code          ───►  git push to main       ───►  Docker Hub    ───►  kubectl apply -f k8s/
  Test Locally                                            (stores built        │
  git push              ┌── Lint (flake8)                Docker image)        ▼
                        ├── Build Docker Image                            Minikube Cluster
                        └── Push to Docker Hub                            └── Flask App Pod
                                                                               (NodePort access)
```

> The deployment target is a **local Minikube cluster**, not a cloud provider.  
> This keeps the setup free and reproducible on any Linux machine.

---

## Tech Stack

| Tool | Role |
|---|---|
| **Python 3.11 + Flask** | The web application |
| **Docker** | Containerises the app into a portable image |
| **Docker Hub** | Stores the built Docker images (image registry) |
| **GitHub Actions** | Automates linting, building, and pushing on every commit |
| **Minikube** | Runs a local Kubernetes cluster for deployment practice |
| **kubectl** | CLI tool used to manually deploy and manage the app on Minikube |
| **Linux** | Operating environment for all tooling |

---

## Project Structure

```
DevOps-Projects/
└── Project-01/                         ← This repository
    ├── .github/
    │   └── workflows/
    │       └── project-01-ci.yml       ← GitHub Actions CI pipeline
    ├── Sample_Flask_app/
    │   ├── k8/
    │   │   ├── deployment.yaml         ← Kubernetes Deployment manifest
    │   │   └── service.yaml            ← Kubernetes Service manifest (NodePort)
    │   ├── .dockerignore
    │   ├── app.py                      ← Flask application
    │   ├── Dockerfile                  ← Container build recipe
    │   └── requirements.txt            ← Python dependencies
    ├── .gitignore
    └── README.md
```

---

## Prerequisites

Make sure the following are installed on your Linux machine before starting:

- [Python 3.11+](https://www.python.org/)
- [Docker](https://docs.docker.com/engine/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Git](https://git-scm.com/)
- A [Docker Hub](https://hub.docker.com/) account
- A [GitHub](https://github.com/) account

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Abdullah-Abid-03/DevOps-Projects.git
cd DevOps-Projects/Project-01/Sample_Flask_app
```

**Also download the workflow file from  `.github/workflows/project-01-ci.yml` for Project- 01** and place it in the same folder as the project at root level.

### 2. Run the Flask App Locally (bare Python)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 app.py
```

Test the routes:

```bash
curl http://localhost:5000/         # Hello, World! 🚀
curl http://localhost:5000/health   # {"status": "healthy"}
curl http://localhost:5000/metrics  # Prometheus metrics text
```

---

## Docker

### Build the Image Locally

```bash
# From inside Sample_Flask_app/
docker build -t my-flask-app:v1 .
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name flask-test my-flask-app:v1

curl http://localhost:5000/

# Clean up
docker stop flask-test && docker rm flask-test
```

### Push to Docker Hub (manual)

```bash
docker login
docker tag my-flask-app:v1 YOUR_USERNAME/my-flask-app:v1
docker push YOUR_USERNAME/my-flask-app:v1
```

> In normal workflow you **do not** need to do this manually.  
> The CI pipeline (GitHub Actions) handles building and pushing automatically on every commit.

---

## CI Pipeline — GitHub Actions

The workflow file lives at `.github/workflows/project-01-ci.yml`.

**It is triggered automatically on every push to `main` that touches `Project-01/` files.**

### What the pipeline does, step by step:

| Step | What happens |
|---|---|
| **Checkout** | Downloads your latest code onto the GitHub runner machine |
| **Setup Python** | Installs Python 3.11 on the runner |
| **Install dependencies** | Runs `pip install` for the app requirements |
| **Lint** | Runs `flake8` to check for Python code style errors |
| **Docker login** | Authenticates with Docker Hub using GitHub Secrets |
| **Build & Push** | Builds the Docker image and pushes it to Docker Hub tagged with the commit SHA and `latest` |

### GitHub Secrets required

Go to your GitHub repo → **Settings → Secrets and variables → Actions** and add:

| Secret name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | A Docker Hub access token (not your password) |

---

## Kubernetes Deployment (Manual — Minikube)

> This is the **Continuous Delivery** step — done manually after CI has built and pushed a new image.

### 1. Start Minikube

```bash
minikube start --driver=docker

# Verify the cluster is up
kubectl get nodes
# Expected: minikube   Ready   control-plane
```

### 2. Deploy the Application

```bash
# From the Project-01/ root
kubectl apply -f Sample_Flask_app/k8/

# Watch the pod start up (Ctrl+C to stop watching)
kubectl get pods -w
# Wait until STATUS shows: Running
```

### 3. Access the App in Your Browser

```bash
minikube service flask-app-service

# Or get just the URL
minikube service flask-app-service --url
```

### 4. Useful kubectl Commands

```bash
# Check pod status and restart count
kubectl get pods

# Detailed pod info + events (great for debugging)
kubectl describe pod <pod-name>

# Stream live logs from the app
kubectl logs <pod-name> -f

# Check the service
kubectl get services

# Delete and let Kubernetes recreate the pod
kubectl delete pod <pod-name>

# Apply updated manifests after changing a YAML file
kubectl apply -f Sample_Flask_app/k8/
```

### 5. Update to a New Image Version

After CI pushes a new `:latest` image, pull it into your running cluster:

```bash
kubectl rollout restart deployment/flask-app

# Confirm the rollout completed
kubectl rollout status deployment/flask-app
```

### 6. Tear Down

```bash
# Remove all deployed resources
kubectl delete -f Sample_Flask_app/k8/

# Stop the Minikube cluster
minikube stop
```

---

## Application Endpoints

| Route | Method | Description |
|---|---|---|
| `/` | GET | Returns `Hello, World! 🚀` with HTTP 200 |
| `/health` | GET | Health check — returns `{"status": "healthy"}` |
| `/metrics` | GET | Prometheus-format metrics (request counters, process stats) |

---

## What's Not Included in This Version

The following are **planned for future iterations** of this project:

- [ ] **Prometheus** — metrics scraping and storage
- [ ] **Grafana** — live dashboards for CPU, memory, and network
- [ ] **Chaos Engineering** — intentional failure scenarios (OOMKilled, ImagePullBackOff, CrashLoopBackOff, node failure, etc.)
- [ ] **Helm** — packaging Kubernetes manifests into a chart
- [ ] **Horizontal Pod Autoscaler** — automatic scaling under load

---


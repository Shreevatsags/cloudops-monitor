# CloudOps Monitor

CloudOps Monitor is a full-stack DevOps and Cloud Operations platform for managing applications, CI/CD pipelines, Docker images, and Kubernetes deployments.

The project combines React, FastAPI, PostgreSQL, Docker, Jenkins, Kubernetes, Terraform, and AWS to demonstrate an end-to-end DevOps workflow.

## Architecture

![CloudOps Monitor Architecture](docs/architecture.png)

The overall architecture follows this flow:

Developer → GitHub → Jenkins CI/CD → Amazon ECR → Amazon EKS → Application

The CloudOps Monitor dashboard communicates with the FastAPI backend. The backend manages applications and deployments and triggers Jenkins pipelines. Jenkins builds Docker images and pushes them to Amazon ECR. Kubernetes runs the application containers inside Amazon EKS.

## Project Overview

CloudOps Monitor provides a centralized interface for application deployment and management.

The platform allows users to:

- Register applications
- Store GitHub repository URLs
- Trigger application builds
- Build Docker images using Jenkins
- Push Docker images to Amazon ECR
- Receive build information through a FastAPI callback
- Deploy applications to Kubernetes
- Create Kubernetes Services
- View deployment status
- View application logs
- Stop deployments
- Restart deployments
- Monitor applications and deployments from the dashboard

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected API endpoints

### Application Management

- Create applications
- View application details
- Store GitHub repository URLs
- Track application build status
- Store Docker image information
- Trigger Jenkins builds

### Deployment Management

- Create deployments
- View deployment details
- View deployment status
- View deployment logs
- Stop deployments
- Restart deployments
- Track Kubernetes deployment names

### CI/CD

- Jenkins-based CI/CD
- GitHub repository cloning
- Automated Docker image builds
- Amazon ECR authentication
- Docker image publishing
- FastAPI build callback
- Backend Docker image build
- Automated backend deployment to Kubernetes
- Kubernetes rollout verification

### Kubernetes

- Kubernetes Deployments
- Kubernetes Services
- Kubernetes RBAC
- Application Pods
- LoadBalancer Services
- MySQL deployment
- PostgreSQL deployment
- Application restart and stop operations

### Dashboard

The dashboard provides:

- Total applications
- Total deployments
- Running deployments
- System health
- Application information
- Deployment information

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- React Router

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- JWT Authentication

### DevOps

- Git
- GitHub
- Docker
- Docker Compose
- Jenkins
- Kubernetes
- kubectl
- Minikube

### AWS

- Amazon EKS
- Amazon ECR
- Amazon VPC
- Amazon EC2
- AWS IAM
- AWS LoadBalancer
- AWS CLI

### Infrastructure as Code

- Terraform

### Web Server

- Nginx

## CI/CD Pipeline

CloudOps Monitor contains two major Jenkins pipelines.

### Application CI/CD Pipeline

The application pipeline takes an application's GitHub repository and produces a Docker image in Amazon ECR.

```text
GitHub Repository
       |
       v
    Jenkins
       |
       v
Validate Parameters
       |
       v
Clone Repository
       |
       v
Build Docker Image
       |
       v
Login to Amazon ECR
       |
       v
Push Docker Image
       |
       v
Notify FastAPI
       |
       v
Application Image Ready
```

The application pipeline performs:

1. Validate Parameters
2. Clone Repository
3. Build Docker Image
4. Login to Amazon ECR
5. Push Image to ECR
6. Notify FastAPI

### Backend CI/CD Pipeline

The backend pipeline builds and deploys the CloudOps Monitor FastAPI backend.

```text
CloudOps Monitor Repository
            |
            v
         Jenkins
            |
            v
   Build Backend Image
            |
            v
       Amazon ECR
            |
            v
        Amazon EKS
            |
            v
   Kubernetes Rollout
```

The backend pipeline performs:

1. Clone CloudOps Monitor repository
2. Build backend Docker image
3. Login to Amazon ECR
4. Push backend image
5. Update Kubernetes deployment
6. Verify Kubernetes rollout

## Kubernetes Architecture

Applications are deployed using Kubernetes Deployments and Services.

```text
                  Kubernetes
                      |
          +-----------+-----------+
          |                       |
          v                       v
    CloudOps Backend        User Application
          |                       |
          v                       v
      PostgreSQL                MySQL
```

For a two-tier application:

```text
              AWS LoadBalancer
                     |
                     v
             Flask Application
                     |
                     v
              mysql-service
                     |
                     v
                  MySQL
```

The Flask application communicates with MySQL using the Kubernetes service name instead of localhost.

## Kubernetes RBAC

The CloudOps backend uses a Kubernetes ServiceAccount with RBAC permissions.

The backend ServiceAccount can manage the required Kubernetes resources such as:

- Deployments
- Pods
- Services

This allows the FastAPI backend to create, inspect, restart, and delete application deployments through the Kubernetes API.

## Database Architecture

CloudOps Monitor uses PostgreSQL as the primary database for the platform.

PostgreSQL stores:

- Users
- Applications
- Deployments

The deployed two-tier Flask application uses MySQL as its application-specific database.

```text
CloudOps Monitor
      |
      v
  PostgreSQL


Deployed Application
      |
      v
     MySQL
```

## Authentication Flow

The application uses JWT authentication.

```text
User
 |
 | Login
 v
FastAPI
 |
 | JWT Token
 v
React Frontend
 |
 | Authorization Header
 v
Protected API
```

Protected requests use:

```text
Authorization: Bearer <JWT_TOKEN>
```

## Deployment Workflow

The complete application deployment workflow is:

```text
1. User creates an application
              |
              v
2. GitHub repository is stored
              |
              v
3. User triggers Build
              |
              v
4. FastAPI triggers Jenkins
              |
              v
5. Jenkins clones GitHub repository
              |
              v
6. Jenkins builds Docker image
              |
              v
7. Jenkins pushes image to Amazon ECR
              |
              v
8. Jenkins notifies FastAPI
              |
              v
9. FastAPI stores Docker image
              |
              v
10. User deploys application
              |
              v
11. Kubernetes Deployment is created
              |
              v
12. Kubernetes Service is created
              |
              v
13. Application Pod starts
              |
              v
14. Application becomes accessible
```

## Deployment Management

CloudOps Monitor provides deployment controls through the dashboard.

Each deployment provides:

- Deployment ID
- Application ID
- Version
- Status
- Kubernetes deployment name
- Start time
- Logs

Available operations:

- Create deployment
- Stop deployment
- Restart deployment
- View logs
- View deployment details

## AWS Infrastructure

The project was deployed and tested using:

- Amazon EKS
- Amazon ECR
- Amazon VPC
- AWS IAM
- Amazon EC2
- AWS LoadBalancer

The AWS infrastructure included:

```text
AWS VPC
 |
 +-- Public Subnets
 |
 +-- Private Subnets
 |
 +-- Internet Gateway
 |
 +-- NAT Gateway
 |
 +-- EKS Cluster
       |
       +-- EKS Node Group
       |
       +-- CloudOps Backend
       |
       +-- PostgreSQL
       |
       +-- User Applications
```

## Infrastructure as Code

Terraform was used to provision and manage the AWS infrastructure.

Typical Terraform workflow:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

After completing AWS deployment and testing, the infrastructure was destroyed to avoid unnecessary ongoing cloud costs:

```bash
terraform destroy
```

The AWS infrastructure used for this project has been removed after testing.

## AWS Deployment Flow

```text
React Dashboard
       |
       v
FastAPI Backend
       |
       v
Jenkins
       |
       v
Docker Image
       |
       v
Amazon ECR
       |
       v
Amazon EKS
       |
       v
AWS LoadBalancer
       |
       v
Deployed Application
```

## Demonstrated Application

A two-tier Flask application was successfully deployed to Kubernetes.

The application consisted of:

```text
Flask Application
        |
        v
    MySQL Database
```

The Flask application was exposed through a Kubernetes LoadBalancer Service and successfully tested through its external AWS endpoint.

## Local Development

### Prerequisites

Install:

- Git
- Docker Desktop
- Python
- Node.js
- Docker Compose
- kubectl
- Minikube
- Terraform
- AWS CLI

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd cloudops-monitor
```

### Run with Docker Compose

```bash
docker compose up --build
```

Docker Compose runs:

```text
React Frontend
      |
      v
FastAPI Backend
      |
      v
PostgreSQL
```

The frontend is served using Nginx.

## Kubernetes Local Development

Start Minikube:

```bash
minikube start --driver=docker
```

Check the cluster:

```bash
kubectl get nodes
```

Apply Kubernetes configurations:

```bash
kubectl apply -f k8s/
```

Check Pods:

```bash
kubectl get pods
```

Check Services:

```bash
kubectl get svc
```

## Project Structure

```text
cloudops-monitor/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── Dockerfile
│   └── package.json
│
├── k8s/
│   ├── deployment.yaml
│   ├── cloudops-rbac.yaml
│   └── mysql.yaml
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Screenshots

### CloudOps Monitor Dashboard

![CloudOps Monitor Dashboard](docs/screenshots/dashboard.png)

### Application Details

![Application Details](docs/screenshots/application-details.png)

### Deployment Details

![Deployment Details](docs/screenshots/deployment-details.png)

### Jenkins Application CI/CD

![Jenkins Application CI/CD](docs/screenshots/jenkins-application.png)

### Jenkins Backend CI/CD

![Jenkins Backend CI/CD](docs/screenshots/jenkins-backend.png)

### Kubernetes Pods

![Kubernetes Pods](docs/screenshots/kubernetes-pods.png)

### Kubernetes Services

![Kubernetes Services](docs/screenshots/kubernetes-services.png)

### Deployed Flask Application

![Deployed Flask Application](docs/screenshots/deployed-application.png)

## Testing

The project was tested across multiple layers.

### Backend Testing

The FastAPI backend was tested using Swagger/OpenAPI.

API functionality included:

- Authentication
- Application creation
- Application retrieval
- Application build triggering
- Jenkins callback
- Deployment creation
- Deployment status
- Deployment logs
- Deployment stop
- Deployment restart

### Jenkins Testing

The Jenkins pipelines were tested for:

- GitHub cloning
- Docker image creation
- ECR authentication
- ECR image publishing
- FastAPI callback
- Backend Kubernetes deployment
- Kubernetes rollout

### Kubernetes Testing

Kubernetes resources were verified using:

```bash
kubectl get pods
kubectl get svc
kubectl get deployments
```

The deployed Flask application was successfully tested through its external LoadBalancer endpoint.

## DevOps Concepts Demonstrated

This project demonstrates practical knowledge of:

- Git
- GitHub
- Git branching
- Git commits
- Docker
- Docker Compose
- Docker image management
- Jenkins
- CI/CD
- Continuous Integration
- Continuous Deployment
- Amazon ECR
- Amazon EKS
- Kubernetes
- Kubernetes Deployments
- Kubernetes Services
- Kubernetes RBAC
- Kubernetes Secrets
- PostgreSQL
- MySQL
- FastAPI
- React
- JWT Authentication
- Terraform
- Infrastructure as Code
- AWS IAM
- AWS VPC
- AWS LoadBalancing
- AWS CLI
- Minikube
- kubectl
- Nginx

## Key Project Highlights

### Full-Stack Platform

React provides the frontend dashboard while FastAPI provides the backend REST API.

### Automated Application Builds

Users can trigger Jenkins builds directly from the CloudOps Monitor application.

### Docker-Based CI/CD

Jenkins automatically builds Docker images from application repositories.

### Amazon ECR Integration

Built Docker images are pushed to Amazon ECR.

### Kubernetes Deployment

Applications are deployed using Kubernetes Deployments and Services.

### Two-Tier Application

The project successfully deployed a Flask application with a MySQL database.

### Deployment Controls

The dashboard provides deployment stop, restart, status, and log functionality.

### Infrastructure as Code

Terraform was used to provision and manage AWS infrastructure.

## Security

The project uses:

- JWT authentication
- Kubernetes RBAC
- AWS IAM
- Kubernetes Secrets
- Environment-based configuration
- Protected API endpoints

Never commit sensitive information to GitHub.

Never commit:

```text
.env
AWS access keys
AWS secret keys
JWT tokens
Jenkins API tokens
ngrok authentication tokens
Database passwords
Private credentials
```

## Project Status

The project has completed its planned implementation and testing.

The following workflow has been successfully demonstrated:

```text
React
  |
  v
FastAPI
  |
  v
Jenkins
  |
  v
Docker
  |
  v
Amazon ECR
  |
  v
Amazon EKS
  |
  v
Kubernetes Application
  |
  v
AWS LoadBalancer
```

The AWS infrastructure used during testing was intentionally destroyed after completion to prevent unnecessary ongoing cloud costs.

The source code, Kubernetes configuration, Terraform configuration, and CI/CD configuration remain available in the GitHub repository.

## Future Improvements

Possible future improvements include:

- Prometheus monitoring
- Grafana dashboards
- Centralized logging
- Kubernetes metrics
- GitHub webhook-triggered builds
- Automated unit and integration testing
- HTTPS/TLS
- Production-grade secrets management
- Blue-green deployments
- Canary deployments
- Application health checks
- Advanced alerting

## Learning Outcomes

This project provides practical experience in building and deploying a complete DevOps platform.

Key learning outcomes include:

- Building REST APIs with FastAPI
- Developing a React frontend
- Implementing JWT authentication
- Working with PostgreSQL
- Containerizing applications with Docker
- Creating CI/CD pipelines with Jenkins
- Managing Docker images with Amazon ECR
- Deploying applications to Amazon EKS
- Creating Kubernetes Deployments and Services
- Configuring Kubernetes RBAC
- Deploying a two-tier application
- Provisioning cloud infrastructure using Terraform
- Managing AWS resources using AWS CLI
- Troubleshooting Docker, Kubernetes, Jenkins, and AWS deployment issues

## Author

**Shreevatsa**

CloudOps Monitor

Full-Stack DevOps & Cloud Deployment Platform
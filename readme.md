# Flask App Deployment to Amazon ECS with Terraform  

# Table of Contents  
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Infrastructure Overview](#infrastructure-overview)
- [App Overview](#app-overview)
- [Pushing Docker Image to ECR](#pushing-docker-image-to-ecr)
- [Setting up Terraform](#setting-up-terraform)
- [Terraform Resources](#terraform-resources)
- [Deploying the App](#deploying-the-app)
- [Accessing the App](#accessing-the-app)
- [Troubleshooting](#troubleshooting)

# Project Overview

Just a basic Flask app that shows the name and the version number. App is Dockerized and deployed to 2 ECS instances using Fargate. An Application Load Balancer handles the ingress/egress, and the app is connected to an RDS MySQL database. 

# Prerequisites

Before proceeding, ensure you have the following:

- An AWS account
- Terraform installed ([Terraform installation guide](https://learn.hashicorp.com/tutorials/terraform/install-cli))
- AWS CLI installed and configured ([AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))
- Docker installed ([Docker installation guide](https://docs.docker.com/get-docker/))

# Infrastructure Overview 

The following AWS resources are provisioned via Terraform:

1. Amazon ECS Cluster: Hosts the Flask app as Fargate tasks.
2. Application Load Balancer (ALB): Balances traffic between two ECS instances.
3. Amazon RDS (MySQL): Provides a MySQL database backend for the Flask app.
4. VPC, Subnets, and Security Groups: Configures networking for the ECS cluster and RDS database.

# Pushing Docker Image to ECR

Before deploying with Terraform, the Docker image for the Flask app needs to be built and pushed to Amazon ECR (Elastic Container Registry).

1. Authenticate Docker to ECR:
   aws ecr get-login-password --region 'region' | docker login --username AWS --password-stdin 'aws_account_id'.dkr.ecr.'region'.amazonaws.com

OPTIONAL*Create the ECR repo

aws ecr create-repository --repository-name 'reponame' --region 'region'

2. Build Docker image:
   docker build -t 'nameimage' .

3. **Tag the Docker image**:
   docker tag 'imagename':latest 'aws_account_id'.dkr.ecr.'region'.amazonaws.com/'imagename':latest

4. **Push the image to ECR**:
   docker push 'aws_account_id'.dkr.ecr.'region'.amazonaws.com/'imagename':latest


# Setting up Terraform

1. Clone this repository to your local machine.

2. Initialize Terraform in the project directory:
   terraform init
   terraform validate

3. Review the `main.tf` file to ensure the AWS region and other parameters fit your environment.

# Terraform Resources

# Key Components Defined in `main.tf`:

- VPC & Subnets: A VPC and two public subnets to host ECS tasks and the RDS database.
- Security Groups: Allows HTTP (port 80) and MySQL (port 3306) traffic.
- ECS Cluster: Runs the Flask app using Fargate.
- Task Definition: Defines the ECS task that runs the Flask app.
- ECS Service: Ensures that two instances of the Flask app are running.
- Application Load Balancer (ALB): Distributes traffic between the two ECS tasks.
- RDS MySQL: Provides a MySQL database backend for the application.

# Deploying the App

1. Apply the Terraform configuration:
    terraform plan
    terraform apply

2. Once the deployment completes, Terraform will output the DNS name of the Application Load Balancer (ALB).

# Accessing the App

After deployment, you can access the Flask app using the DNS name of the Application Load Balancer. 

Example URL: http://<alb_dns_name>

Replace `<alb_dns_name>` with the DNS name provided in the Terraform output (or retrieve it from the AWS Console).

# Troubleshooting

# Common Issues:

1. Containers not running:
   - Check the ECS Task details in the AWS Console for any errors in the task definition or execution.
   - Ensure the Docker image is properly pushed to ECR.

2. Load Balancer Health Check Fails:
   - Verify that your Flask app is properly listening on port 5000.
   - Ensure that the security group for the ECS service allows traffic on port 80.

3. Database connection issues:
   - Verify that the RDS endpoint is correctly set in the ECS task environment variable `DB_HOST`.
   - Ensure that the security group allows inbound traffic on port 3306 for the RDS MySQL instance.

# Debugging with AWS Console:
- Check logs for ECS tasks in Amazon CloudWatch to view any runtime errors or logs from your Flask app.
- Inspect the ALB target group health checks and ensure that your ECS instances are healthy.

# Clean Up

To avoid ongoing charges for the AWS resources provisioned, destroy the infrastructure when you're done:

terraform destroy

This will remove all the AWS resources created by the Terraform configuration.


![alt text](https://github.com/BekeAtGithub/flaskECS/blob/master/FlaskECS.png)

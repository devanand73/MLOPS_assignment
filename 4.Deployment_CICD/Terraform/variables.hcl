variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  default     = "mlops-cluster"
}

variable "node_instance_type" {
  description = "Instance type for EKS nodes"
  default     = "t3.medium"
}

variable "docker_image" {
  description = "Docker image for the application"
  default     = "your-ecr-repo/mlops-app:latest"
}
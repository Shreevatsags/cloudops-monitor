output "ecr_repository_url" {
  description = "ECR repository URL for CloudOps application"
  value       = aws_ecr_repository.cloudops.repository_url
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.cloudops.name
}

output "eks_cluster_endpoint" {
  description = "EKS cluster API endpoint"
  value       = aws_eks_cluster.cloudops.endpoint
}
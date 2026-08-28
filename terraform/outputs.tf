output "ecr_repository_url" {
  description = "ECR repository URL for CloudOps application"
  value       = aws_ecr_repository.cloudops.repository_url
}
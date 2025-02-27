output "cluster_name" {
  value = aws_eks_cluster.mlops.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.mlops.endpoint
}

output "service_loadbalancer" {
  value = kubernetes_service.app.status[0].load_balancer[0].ingress[0].hostname
}
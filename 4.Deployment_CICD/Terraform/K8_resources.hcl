# Namespace
resource "kubernetes_namespace" "mlops" {
  metadata {
    name = "mlops"
  }
}

# Deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name      = "mlops-app"
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "mlops-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "mlops-app"
        }
      }

      spec {
        container {
          name  = "mlops-app"
          image = var.docker_image
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

# Service
resource "kubernetes_service" "app" {
  metadata {
    name      = "mlops-service"
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  spec {
    selector = {
      app = "mlops-app"
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "LoadBalancer"
  }
}
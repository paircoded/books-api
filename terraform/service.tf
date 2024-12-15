resource "kubernetes_service" "books_api" {
  metadata {
    name      = "books-api"
    namespace = "paircoded"
    labels = {
      AppName = "books-api"
    }
  }

  spec {
    selector = {
      AppName = kubernetes_deployment.books_api.metadata.0.labels.AppName
    }
    session_affinity = "ClientIP"
    port {
      port        = 80
      target_port = 80
      protocol    = "TCP"
    }
    type = "NodePort"
  }
}

resource "kubernetes_ingress_v1" "books_api" {
  wait_for_load_balancer = true
  metadata {
    name      = "books-api"
    namespace = "paircoded"
    labels = {
      AppName = "books-api"
    }
  }

  spec {
    ingress_class_name = "nginx"

    tls {
      hosts      = [
        "books-api.paircoded.com"
      ]
      secret_name = "wildcard-paircoded-com"
    }

    rule {
      host = "books-api.paircoded.com"
      http {
        path {
          path = "/"
          backend {
            service {
              name = kubernetes_service.books_api.metadata.0.name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment" "books_api" {
  metadata {
    name      = "books-api"
    namespace = "paircoded"
    labels = {
      AppName = "books-api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        AppName = "books-api"
      }
    }

    template {
      metadata {
        namespace = "paircoded"
        name      = "books-api"
        labels = {
          AppName = "books-api"
        }
        annotations = {
          "instrumentation.opentelemetry.io/inject-python" = "true"
        }
      }

      spec {
        image_pull_secrets {
          name = "regcred"
        }
        container {
          image = "docker-registry.poorlythoughtout.com/books-api:${var.image_tag}"
          image_pull_policy = "Always"
          name  = "books-api"
          port {
            container_port = 80
          }

          env {
            name = "olis_ollama_url"
            value = "http://192.168.1.14:11434"
          }

          env {
            name = "olis_ollama_model"
            value = "impulse2000/dolphin-2.8-experiment26:q6_0_k"
          }
        }
      }
    }
  }
}

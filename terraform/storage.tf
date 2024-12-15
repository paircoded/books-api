resource "kubernetes_persistent_volume_claim" "book_storage" {
  metadata {
    name = "book-storage"
    namespace = "paircoded"
  }
  spec {
    access_modes = ["ReadWriteMany"]
    storage_class_name = "local-storage"
    volume_name = kubernetes_persistent_volume.book_storage.metadata[0].name
    resources {
      requests = {
        storage = "20Gi"
      }
    }
  }
}


resource "kubernetes_persistent_volume" "book_storage" {
  metadata {
    name = "book-storage"
  }
  spec {
    capacity = {
      storage = "20Gi"
    }
    volume_mode = "Filesystem"
    storage_class_name = "local-storage"
    access_modes = ["ReadWriteMany"]
    persistent_volume_source {
      local {
        path = "/mnt/datadisk/book_storage"
      }
    }
    node_affinity {
      required {
        node_selector_term {
          match_expressions {
            key      = "kubernetes.io/hostname"
            operator = "In"
            values = ["k8s-master.internal.poorlythoughtout.com"]
          }
        }
      }
    }
  }
}

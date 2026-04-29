from kubernetes import client, config

def list_nodes():
    try:
        # Carga la configuración que descargaste con gcloud
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        print("☸️ Conectado al clúster de Kubernetes.")
        print("Listing nodes:")
        nodes = v1.list_node()
        for node in nodes.items:
            status = node.status.conditions[-1].type if node.status.conditions else "Unknown"
            print(f"✅ Nodo: {node.metadata.name} | Estado: {status}")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    list_nodes()

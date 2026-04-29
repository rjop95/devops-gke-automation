from kubernetes import client, config

def get_network_info():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    print("🌐 --- RECURSOS DE RED DEL CLÚSTER ---")
    
    # 1. Obtener IPs de los Nodos (Internal/External)
    nodes = v1.list_node()
    for node in nodes.items:
        for addr in node.status.addresses:
            print(f"🖥️  Nodo: {node.metadata.name} | {addr.type}: {addr.address}")

    # 2. Obtener IPs Públicas de Servicios (Load Balancers)
    services = v1.list_service_for_all_namespaces()
    for svc in services.items:
        if svc.status.load_balancer.ingress:
            ip = svc.status.load_balancer.ingress[0].ip
            print(f"🚀 App Disponible en: http://{ip}")

if __name__ == "__main__":
    get_network_info()

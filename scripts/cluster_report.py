from kubernetes import client, config
import datetime

def generate_report():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    nodes = v1.list_node()
    pods = v1.list_pod_for_all_namespaces()
    
    print(f"📊 --- REPORTE DE SALUD DEL CLÚSTER ({datetime.date.today()}) ---")
    print(f"🖥️  Nodos activos: {len(nodes.items)}")
    print(f"📦 Total de Pods (todas las namespaces): {len(pods.items)}")
    
    # Verificamos si hay pods con problemas
    troubled_pods = [p for p in pods.items if p.status.phase not in ['Running', 'Succeeded']]
    
    if not troubled_pods:
        print("✅ Estado General: SALUDABLE")
    else:
        print(f"⚠️  Estado General: ATENCIÓN ({len(troubled_pods)} pods en estado no-Ready)")

if __name__ == "__main__":
    generate_report()

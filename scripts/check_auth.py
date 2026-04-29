import os

def verify_kubeconfig():
    kube_path = os.path.expanduser('~/.kube/config')
    
    print("🔐 Verificando credenciales de acceso...")
    if os.path.exists(kube_path):
        size = os.path.getsize(kube_path)
        print(f"✅ Archivo kubeconfig encontrado ({size} bytes).")
        # Leemos el archivo para ver si tiene el nombre de nuestro clúster
        with open(kube_path, 'r') as f:
            if 'devops-cluster' in f.read():
                print("🎯 El contexto está configurado correctamente para 'devops-cluster'.")
            else:
                print("⚠️ El archivo existe pero no parece tener el clúster actual.")
    else:
        print("❌ No se encontró el archivo de configuración. El comando gcloud falló o no se ha corrido.")

if __name__ == "__main__":
    verify_kubeconfig()

import requests
import sys
import time

def check_site(url):
    print(f"--- Iniciando validación de salud en: {url} ---")
    try:
        # Reintenta hasta 5 veces si el balanceador aún se está configurando
        for i in range(5):
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ ÉXITO: El sitio respondió con código 200.")
                print(f"Contenido recibido: {response.text}")
                return True
            else:
                print(f"⚠️ Intento {i+1}: El sitio respondió con código {response.status_code}. Reintentando...")
                time.sleep(10)
    except Exception as e:
        print(f"❌ ERROR: No se pudo conectar al sitio. Detalle: {e}")
    
    return False

if __name__ == "__main__":
    # La URL se pasará como argumento desde Jenkins
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    if check_site(target_url):
        sys.exit(0) # Salida exitosa para Jenkins
    else:
        sys.exit(1) # Salida con error para detener el Pipeline

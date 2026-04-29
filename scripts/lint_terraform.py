import os

def check_missing_project_field(file_path):
    print(f"🔍 Auditando {file_path} en busca de campos obligatorios...")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Verificamos si existe el recurso de Artifact Registry pero falta el campo project
    if "google_artifact_registry_repository" in content and "project =" not in content:
        print("🚨 ERROR: Se encontró un repositorio sin el campo 'project' definido.")
        return False
    
    print("✅ Todo parece en orden.")
    return True

if __name__ == "__main__":
    if not check_missing_project_field('infra/main.tf'):
        exit(1)

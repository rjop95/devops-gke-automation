import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'infra', 'main.tf')

def patch_idempotent():
    if not os.path.exists(FILE_PATH): return

    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()

    new_lines = []
    project_stmt = '  project    = var.project_id\n'
    
    for i, line in enumerate(lines):
        # Solo agregamos la línea si el bloque inicia Y la siguiente línea no es ya el project
        new_lines.append(line)
        if 'resource "' in line and '{' in line:
            # Verificamos si la siguiente línea ya tiene el project para no duplicar
            if i+1 < len(lines) and 'project' not in lines[i+1]:
                new_lines.append(project_stmt)

    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
    print("✅ Parche aplicado de forma idempotente (sin duplicados).")

if __name__ == "__main__":
    patch_idempotent()

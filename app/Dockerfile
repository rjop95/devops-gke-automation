# 1. Usar una imagen base liviana de Python
FROM python:3.11-slim

# 2. Instalar dependencias del sistema necesarias para compilar componentes de Postgres si hiciera falta
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar el archivo de requerimientos desde el entorno local
COPY src/requirements.txt .

# 5. Instalar las librerías de Python (Flask, SQLAlchemy, psycopg2)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código fuente de la carpeta src al directorio de trabajo
COPY src/ .

# 7. Exponer el puerto en el que corre tu aplicación Flask
EXPOSE 8080

# 8. Comando para arrancar la aplicación apuntando al archivo app.py copiado
CMD ["python", "app.py"]

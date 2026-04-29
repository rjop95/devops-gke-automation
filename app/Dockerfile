# Usamos una versión "slim" de Python para que la imagen sea pequeña y segura
FROM python:3.10-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos Flask directamente (para este ejercicio rápido)
RUN pip install --no-cache-dir flask

# Copiamos solo el archivo de la app al contenedor
COPY main.py .

# Exponemos el puerto que usa Flask
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]

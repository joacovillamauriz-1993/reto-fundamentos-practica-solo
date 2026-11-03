# 1. Imagen base ligera de Python 3.12
FROM python:3.12-slim

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código del proyecto al contenedor
COPY . .

# 5. Comando por defecto para ejecutar el script principal de Python
CMD ["python", "main.py"]


















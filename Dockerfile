FROM python:3.12-slim

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo el archivo de dependencias
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto
COPY . /app/

# Configuración para evitar el almacenamiento en búfer de salida de Python
ENV PYTHONUNBUFFERED=1

# Expone el puerto para la aplicación
EXPOSE 8000

# Comando por defecto para iniciar la aplicación
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]

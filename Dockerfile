# syntax=docker/dockerfile:1
# FROM python:3
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/


# syntax=docker/dockerfile:1
FROM python:3

# Establece las variables de entorno para el usuario no root
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea un usuario no root y establece su directorio de inicio
RUN useradd --create-home appuser
WORKDIR /code

# Copia los archivos requeridos y cambia la propiedad al usuario no root
COPY --chown=appuser:appuser requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade revChatGPT
# install gunicorn
RUN pip install gunicorn

# Copia los archivos restantes y cambia la propiedad al usuario no root
COPY --chown=appuser:appuser . /code/

# copia el archivo config a $HOME/.config/revChatGPT/config.json
COPY --chown=appuser:appuser config.json /home/appuser/.config/revChatGPT/config.json


# Cambia al usuario no root
USER appuser

# Establece el directorio de trabajo para el usuario no root
WORKDIR /code/

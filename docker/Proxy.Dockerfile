# Usa una imagen base de Golang
FROM golang:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Clona el repositorio del proyecto
RUN git clone https://github.com/acheong08/ChatGPT-Proxy-V4.git

# Cambia al directorio del proyecto
WORKDIR /app/ChatGPT-Proxy-V4

# Compila el proyecto
RUN go build

# Define el comando de inicio cuando el contenedor se ejecute
CMD ["./ChatGPT-Proxy-V4"]

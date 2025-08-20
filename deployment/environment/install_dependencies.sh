#!/bin/bash
# Instalacion de dependencias basicas para observer-core

instalar_dependencias() {
  echo "[+] Instalando dependencias basicas..."

  # Actualizar e instalar paquetes basicos
  sudo apt update
  sudo apt install -y python3 python3-pip python3-venv nginx git 

  # Configurar Nginx para que inicie automaticamente
  sudo systemctl enable nginx
  sudo systemctl start nginx

  echo "[✓] Dependencias instaladas correctamente."
}

instalar_dependencias

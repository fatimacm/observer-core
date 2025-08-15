#!/bin/bash
# Instalacion de dependencias basicas para observer-core
LOG="logs_despliegue.txt"

instalar_dependencias() {
  echo "[+] Instalando dependencias basicas..." | tee -a $LOG

  # Actualizar e instalar paquetes basicos
  sudo apt update >> $LOG 2>&1
  sudo apt install -y python3 python3-pip python3-venv nginx git >> $LOG 2>&1

  # Configurar Nginx para que inicie automaticamente
  sudo systemctl enable nginx >> $LOG 2>&1
  sudo systemctl start nginx >> $LOG 2>&1

  echo "[✓] Dependencias instaladas correctamente." | tee -a $LOG
}

instalar_dependencias

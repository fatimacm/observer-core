#!/bin/bash

LOG="logs_despliegue.txt"

instalar_dependencias() {
  echo "Instalando dependencias..." | tee -a $LOG
  sudo apt update && sudo apt install -y python3 python3-pip python3-venv nginx git >> $LOG 2>&1
  sudo systemctl enable nginx >> $LOG 2>&1
  sudo systemctl start nginx >> $LOG 2>&1
}

instalar_dependencias

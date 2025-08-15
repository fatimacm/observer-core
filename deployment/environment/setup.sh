#!/bin/bash
# setup.sh – Configuracion de entorno virtual para observer-core

# Carpeta interna de repositorio de ejemplo
REPO_DIR="../../repos/devops-static-web"
cd "$REPO_DIR" || exit 1

# Verificar si existe entorno virtual
if [ ! -d "venv" ]; then
  echo "[+] Creando entorno virtual..."
  python3 -m venv venv
  source venv/bin/activate

  # Instalar dependencias de ejemplo
  touch requirements.txt
  echo "# Dependencias de ejemplo" > requirements.txt
  pip install -r requirements.txt || echo "[!] No hay paquetes reales, instalacin simulada"
  pip install gunicorn --quiet
  echo "[✓] Entorno virtual configurado."
else
  echo "[✓] Entorno virtual ya existe. Activando..."
  source venv/bin/activate
fi

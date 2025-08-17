#!/bin/bash
# setup.sh – Configuracion minima del entorno virtual para observer-core

# Directorio del entorno virtual
VENV_DIR="./venv"

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creando entorno virtual en $VENV_DIR ..."
    python3 -m venv $VENV_DIR
else
    echo "[✓] Entorno virtual ya existe en $VENV_DIR"
fi

# Activar entorno virtual(solo para este script)
source $VENV_DIR/bin/activate

# Actualizar pip
echo "[+] Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias minimas
echo "[+] Instalando dependencias basicas (FastAPI, Uvicorn)..."
pip install --quiet fastapi uvicorn psutil

# Confirmacion final
echo "[✓] Entorno listo. Para iniciar la API:"
echo "    source venv/bin/activate"  # Desde root debes hacer esto manualmente
echo "    cd api"
echo "    uvicorn main:app --reload"

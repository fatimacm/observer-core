#!/bin/bash
# init.sh – Inicializacion de repositorio local para observer-core

# Carpeta interna de repositorios de ejemplo
REPO_DIR="../../repos/devops-static-web"

# Verificar si el repositorio ya existe
if [ ! -d "$REPO_DIR" ]; then
  echo "[+] Creando repositorio de ejemplo..."
  mkdir -p "$REPO_DIR"
  # Simular estructura minima del repo
  touch "$REPO_DIR/README.md"
  touch "$REPO_DIR/index.html"
  echo "<!-- Repositorio de ejemplo para observer-core -->" > "$REPO_DIR/README.md"
  echo "<h1>DevOps Static Web - Ejemplo</h1>" > "$REPO_DIR/index.html"
  echo "[✓] Repositorio de ejemplo creado."
else
  echo "[✓] Repositorio ya existe. No se crea nada."
fi

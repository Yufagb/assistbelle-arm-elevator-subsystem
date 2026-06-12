#!/usr/bin/env bash
set -euo pipefail

# Importa los proyectos ESP-IDF desde los ZIP originales hacia la estructura ordenada del repo.
# Uso:
#   cd robot-project
#   bash firmware/import_firmware_from_zips.sh \
#     "/ruta/JointPosition y JointVelocity Controllers.zip" \
#     "/ruta/can-controll-.zip"

if [ "$#" -ne 2 ]; then
  echo "Uso: bash firmware/import_firmware_from_zips.sh <JointPosition y JointVelocity Controllers.zip> <can-controll-.zip>"
  exit 1
fi

JOINT_ZIP="$1"
CAN_ZIP="$2"

if [ ! -f "$JOINT_ZIP" ]; then
  echo "No existe: $JOINT_ZIP"
  exit 1
fi

if [ ! -f "$CAN_ZIP" ]; then
  echo "No existe: $CAN_ZIP"
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "Extrayendo ZIPs en $TMP_DIR"
unzip -q "$JOINT_ZIP" -d "$TMP_DIR/joint"
unzip -q "$CAN_ZIP" -d "$TMP_DIR/can"

mkdir -p firmware/esp32_joint_node/J1
mkdir -p firmware/esp32_joint_node/J2
mkdir -p firmware/esp32_joint_node/J3
mkdir -p firmware/esp32_joint_node/J4
mkdir -p firmware/esp32_stepper_node/J5_tb6600

copy_joint_node() {
  local NODE="$1"
  local SRC="$TMP_DIR/joint/JointVelocityControllers/$NODE"
  local DST="firmware/esp32_joint_node/$NODE"

  if [ ! -d "$SRC" ]; then
    echo "No se encontro $SRC"
    exit 1
  fi

  echo "Copiando $NODE -> $DST"
  mkdir -p "$DST/main"

  cp "$SRC/CMakeLists.txt" "$DST/CMakeLists.txt"
  cp "$SRC/sdkconfig" "$DST/sdkconfig"
  cp "$SRC/main/CMakeLists.txt" "$DST/main/CMakeLists.txt"
  cp "$SRC/main/"*.c "$DST/main/"
  cp "$SRC/main/"*.h "$DST/main/"

  # Mantener README propio si ya existe. Si no existe, copiar el README fuente.
  if [ ! -f "$DST/README.md" ] && [ -f "$SRC/README.md" ]; then
    cp "$SRC/README.md" "$DST/README.md"
  fi
}

copy_joint_node J1
copy_joint_node J2
copy_joint_node J3
copy_joint_node J4

SRC_J5="$TMP_DIR/can/can-controll-"
DST_J5="firmware/esp32_stepper_node/J5_tb6600"

if [ ! -d "$SRC_J5" ]; then
  echo "No se encontro $SRC_J5"
  exit 1
fi

echo "Copiando J5 TB6600 -> $DST_J5"
mkdir -p "$DST_J5/main"
cp "$SRC_J5/CMakeLists.txt" "$DST_J5/CMakeLists.txt"
cp "$SRC_J5/sdkconfig" "$DST_J5/sdkconfig"
cp "$SRC_J5/main/CMakeLists.txt" "$DST_J5/main/CMakeLists.txt"
cp "$SRC_J5/main/Kconfig.projbuild" "$DST_J5/main/Kconfig.projbuild"
cp "$SRC_J5/main/"*.c "$DST_J5/main/"

# Limpieza preventiva: no versionar salidas de build ni configuraciones locales de IDE.
echo "Limpiando archivos no versionables"
find firmware -type d \( -name build -o -name .vscode -o -name .devcontainer \) -prune -exec rm -rf {} +
find firmware -type f \( -name sdkconfig.old -o -name .clangd -o -name "*.bin" -o -name "*.elf" -o -name "*.map" \) -delete

echo "Importacion terminada. Revisa con:"
echo "  git status"
echo "  find firmware/esp32_joint_node firmware/esp32_stepper_node -maxdepth 3 -type f | sort"
echo ""
echo "Luego ejecuta:"
echo "  git add firmware/"
echo "  git commit -m 'Add complete ESP-IDF firmware sources'"
echo "  git push origin hardwarex-publication-package"

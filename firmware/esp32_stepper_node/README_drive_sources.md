# Fuentes de firmware ESP32 del elevador desde Drive

Esta carpeta documenta los codigos ESP32 encontrados para el eje prismatico J5 / sistema de elevacion.

## Carpeta fuente revisada

- Drive: `JointPositionControllers`
- Subcarpetas encontradas:
  - `twai_id_based_basedness`
  - `codigo para diferentes nodos`

## Archivos detectados

En `twai_id_based_basedness` se encontro un proyecto ESP-IDF con:

```text
twai_id_based_basedness/
├── CMakeLists.txt
├── sdkconfig
└── main/
    ├── CMakeLists.txt
    ├── twai_id_based_basedness.c
    └── Kconfig.projbuild
```

En `codigo para diferentes nodos` se encontraron archivos C separados:

```text
nodo1.c
nodo2.c
nodo3.c
nodo4.c
```

## Interpretacion actual

Esta carpeta parece contener codigo de posicionamiento y pruebas por IDs TWAI/CAN. Puede servir como base para documentar el control del elevador y/o nodos individuales.

## Regla para GitHub

No subir carpetas `build/`, `.vscode/`, `.devcontainer/` ni archivos generados. Solo subir codigo fuente y configuracion necesaria.

## Pendiente critico

- Confirmar cual archivo corresponde realmente al nodo J5 del elevador.
- Confirmar pines STEP, DIR y EN usados para los drivers TB6600 o DRV8825.
- Confirmar si el sistema final usa TB6600, DRV8825 o ambos en etapas distintas.
- Confirmar unidad interna de posicion: pasos, milimetros o metros.

## Comando local recomendado

```bash
cd ~/robot-project
git checkout hardwarex-publication-package
mkdir -p firmware/esp32_stepper_node/J5
# Copiar desde Drive solo archivos fuente y CMakeLists necesarios
# No copiar build/ ni carpetas de IDE
git add firmware/esp32_stepper_node
git commit -m "Add ESP32 stepper firmware sources from Drive"
git push origin hardwarex-publication-package
```

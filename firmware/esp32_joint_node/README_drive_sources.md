# Fuentes de firmware ESP32 desde Drive

Esta carpeta documenta los codigos ESP32 encontrados en la carpeta de Drive compartida por el proyecto.

## Carpeta fuente revisada

- Drive: `JointVelocityControllers`
- Subcarpetas encontradas: `J1`, `J2`, `J3`, `J4`, `components`.

## Estructura detectada por articulacion

Cada articulacion contiene una estructura de proyecto ESP-IDF similar:

```text
Jx/
├── CMakeLists.txt
├── sdkconfig
├── main/
│   ├── CMakeLists.txt
│   ├── main.c
│   ├── node_config.h
│   ├── twai_comms.h
│   ├── base_libs.h
│   ├── encoder_driver.h
│   ├── motor_driver.h
│   └── pid_controller.h
└── build/              # no subir a GitHub
```

En J2, J3 y J4 tambien aparecen archivos relacionados al gripper cuando el proyecto incluye esa logica.

## Regla para GitHub

No se deben subir carpetas `build/`, `.vscode/`, `.devcontainer/`, `sdkconfig.old` ni archivos generados. Solo se deben versionar:

- `CMakeLists.txt`
- `sdkconfig` si es necesario para reproducibilidad
- `main/*.c`
- `main/*.h`
- `README.md`

## Estado

Se creo esta guia porque la carpeta de Drive contiene los proyectos completos, pero la importacion directa de archivos `.c` y `.h` desde Drive no entrega el texto en el conector. Para cerrar esta parte, copiar localmente los archivos fuente desde Drive a esta carpeta y hacer commit.

## Comando local recomendado

```bash
cd ~/robot-project
git checkout hardwarex-publication-package
mkdir -p firmware/esp32_joint_node/J1 firmware/esp32_joint_node/J2 firmware/esp32_joint_node/J3 firmware/esp32_joint_node/J4
# Copiar desde Drive solo CMakeLists.txt, sdkconfig y main/*.c main/*.h
# No copiar build/ ni .vscode/
git add firmware/esp32_joint_node
git commit -m "Add ESP32 joint firmware sources from Drive"
git push origin hardwarex-publication-package
```

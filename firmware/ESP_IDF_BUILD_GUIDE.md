# Guia de compilacion ESP-IDF

Esta guia define como debe quedar el firmware para que, al descargar el repositorio, se pueda compilar y programar cada ESP32 desde la rama `hardwarex-publication-package`.

## Recomendacion sobre ESP-IDF

No subir ESP-IDF completo al repositorio. ESP-IDF, sus herramientas, toolchains y contenedores pueden pesar varios GB y son dependencias externas. En GitHub solo debe ir el codigo fuente del proyecto del robot.

Mantener ESP-IDF instalado fuera del repositorio, por ejemplo en:

```text
/media/F15/Data/ESP_IDF_CONTAINER/
/media/F15/Data/ESP_IDF_TOOLS/
```

El repositorio debe ser reproducible indicando como cargar o instalar ESP-IDF, no copiando ESP-IDF dentro del repo.

## Estado actual

El firmware fue recuperado desde los ZIP subidos al chat:

- `JointPosition y JointVelocity Controllers.zip`
- `can-controll-.zip`

Ya se documentaron los pines y se subieron archivos clave de configuracion por nodo. Para dejar cada proyecto completamente compilable, deben estar presentes tambien los archivos fuente restantes de J1 a J4.

## Estructura objetivo

```text
firmware/
├── esp32_joint_node/
│   ├── J1/
│   │   ├── CMakeLists.txt
│   │   └── main/
│   │       ├── CMakeLists.txt
│   │       ├── main.c
│   │       ├── base_libs.h
│   │       ├── node_config.h
│   │       ├── encoder_driver.h
│   │       ├── motor_driver.h
│   │       ├── pid_controller.h
│   │       └── twai_comms.h
│   ├── J2/
│   ├── J3/
│   └── J4/
│       └── main/
│           └── grip_controller.h
└── esp32_stepper_node/
    └── J5_tb6600/
        ├── CMakeLists.txt
        └── main/
            ├── CMakeLists.txt
            ├── Kconfig.projbuild
            └── twai_network_example_slave_main.c
```

## Archivos que no deben subirse

No versionar:

```text
build/
.vscode/
.devcontainer/
sdkconfig.old
.clangd
*.bin
*.elf
*.map
ESP_IDF_CONTAINER/
ESP_IDF_TOOLS/
esp-idf/
.espressif/
```

## Si aparece `idf.py: command not found`

Ese error significa que ESP-IDF no esta cargado en esa terminal o no esta instalado.

Primero buscar el archivo `export.sh` de ESP-IDF:

```bash
find "$HOME" /media/F15/Data -type f -path "*/esp-idf/export.sh" 2>/dev/null
```

Si aparece una ruta, cargarla. Ejemplo segun la instalacion actual del proyecto:

```bash
source /home/f15/projects/tb6600_can_control_vscode/components/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
```

Si ESP-IDF esta en el disco externo, usar la ruta real que devuelva el comando `find`, por ejemplo:

```bash
source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh
```

Despues verificar:

```bash
idf.py --version
echo $IDF_PATH
ls "$IDF_PATH/tools/cmake/project.cmake"
```

Para no repetirlo en cada terminal, agregarlo a `.bashrc` usando la ruta real encontrada:

```bash
echo 'source /media/F15/Data/ESP_IDF_CONTAINER/v5.3.3/esp-idf/export.sh' >> ~/.bashrc
source ~/.bashrc
```

Solo usar esa linea si la ruta existe en tu equipo.

Si no existe ningun `export.sh`, instalar ESP-IDF:

```bash
mkdir -p ~/esp
cd ~/esp
git clone -b v5.3.2 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32
source ./export.sh
idf.py --version
```

Con VS Code tambien se puede instalar desde la extension Espressif IDF:

1. Abrir VS Code.
2. Instalar extension `Espressif IDF`.
3. Ejecutar `ESP-IDF: Configure ESP-IDF Extension`.
4. Usar `Express` setup o apuntar a la ruta existente en el disco externo.
5. Abrir la carpeta de un nodo, por ejemplo `firmware/esp32_joint_node/J1`.
6. Usar `ESP-IDF: Build`, `ESP-IDF: Flash` y `ESP-IDF: Monitor`.

## Compilar un nodo J1-J4

Ejemplo para J1:

```bash
cd firmware/esp32_joint_node/J1
idf.py set-target esp32
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

Cambiar `J1` por `J2`, `J3` o `J4` segun el ESP32 que se desea programar.

## Compilar el elevador J5

```bash
cd firmware/esp32_stepper_node/J5_tb6600
idf.py set-target esp32
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

## Verificar puerto serie

```bash
ls /dev/ttyUSB*
ls /dev/ttyACM*
```

En Linux, si no aparece el puerto o no hay permisos:

```bash
sudo usermod -aG dialout $USER
```

Cerrar sesion y volver a entrar.

## Relacion con ROS 2

- ROS 2 queda en `ros2_ws/`.
- Los ESP32 se programan desde `firmware/`.
- ESP-IDF queda fuera del repositorio como dependencia externa.
- La comunicacion entre ROS 2 y ESP32 se realiza mediante CAN/TWAI a 500 kbit/s.
- La Raspberry Pi usa MCP2515 como interfaz CAN.

## Pendiente

- Subir todos los archivos fuente restantes de J1-J4 para que cada carpeta compile de forma autonoma.
- Confirmar formato final de payload CAN entre ROS 2 y ESP32.
- Confirmar si J5 queda como `J5_tb6600` o si se conservara tambien una version historica `J5_twai_id_based`.

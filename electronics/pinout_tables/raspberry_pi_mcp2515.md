# Raspberry Pi 5 a MCP2515

Tabla extraida de la tesis, Anexo 4: Integracion del MCP2515 con Raspberry Pi 5.

## Mapeo de pines

| MCP2515 | GPIO BCM | Pin fisico Raspberry Pi 5 | Nota |
|---|---:|---:|---|
| VCC | - | 2 / 4 | 5 V en modulos con regulador/transceptor. |
| GND | - | 6 | Tierra comun. |
| CS | GPIO8 | 24 | SPI0 CE0, interfaz can0. |
| SCK | GPIO11 | 23 | Reloj SPI. |
| MOSI | GPIO10 | 19 | Datos hacia MCP2515. |
| MISO | GPIO9 | 21 | Datos desde MCP2515. |
| INT | GPIO25 | 22 | Interrupcion del MCP2515. |

## Configuracion usada en la tesis

```bash
dtparam=spi=on
dtoverlay=spi-bcm2835
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
```

## Puesta en marcha de CAN

```bash
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 500000
ip -details link show can0
```

## Validaciones rapidas

```bash
ls /dev/spidev*
lsmod | grep -i spi
lsmod | grep -E 'mcp251x|can'
sudo modprobe mcp251x
sudo modprobe can_raw
sudo modprobe can_dev
ip link show
candump can0
```

## Notas electricas

- Mantener logica SPI/INT compatible con 3.3 V de Raspberry Pi.
- Usar terminacion de 120 ohmios en cada extremo del bus CAN.
- Todos los nodos deben trabajar con el mismo bitrate.
- En la tesis se empleo 500 kbit/s.

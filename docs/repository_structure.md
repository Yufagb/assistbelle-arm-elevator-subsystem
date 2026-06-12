# Estructura del repositorio

Este archivo define la estructura de trabajo para la rama hardwarex-publication-package.

## Reglas principales

- El codigo de ROS 2 se mantiene en ros2_ws.
- No duplicar paquetes, nodos ni scripts ROS 2 dentro de software.
- El firmware ESP32 final debe ir en firmware.
- Codigo_esp32 se conserva solo como fuente temporal para migrar codigo.
- Los resultados historicos pueden quedarse en resultados.
- Los datasets limpios y publicables deben ir en validation.

## Carpetas principales

- README.md
- requirements.txt
- docs
- hardware
- electronics
- firmware
- ros2_ws
- software
- validation
- paper
- Codigo_esp32
- resultados

## Responsabilidad por carpeta

- hardware: CAD mecanico, STEP, STL, planos, fasteners y fotos mecanicas.
- electronics: esquematicos, cableado, pinouts, potencia e imagenes de electronica.
- firmware: codigo fuente ESP32 y notas del protocolo CAN.
- ros2_ws: workspace ROS 2 completo.
- software: guias de instalacion y scripts auxiliares que no sean ROS 2.
- validation: datasets curados, graficas de validacion y referencias a videos.
- paper: manuscrito, figuras, tablas y referencias.
- docs: manuales, checklists, BOM y documentacion general.

## Reglas de migracion

1. Migrar firmware ESP32 desde Codigo_esp32 hacia firmware.
2. Mantener todo el codigo ROS 2 dentro de ros2_ws.
3. Copiar solo datos curados desde resultados hacia validation.
4. Colocar figuras finales del manuscrito en paper/figures.
5. Usar carpetas mecanicas en minuscula: hardware/cad, hardware/step y hardware/stl.

## Carpetas antiguas

No agregar archivos nuevos en hardware/CAD_editable, hardware/STEP ni hardware/STL.

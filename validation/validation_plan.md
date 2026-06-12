# Plan de validación

Este documento define las pruebas mínimas necesarias para respaldar el paquete de publicación HardwareX.

## Objetivo general

Validar que el robot puede ejecutar movimientos reproducibles mediante ROS 2, bus CAN y firmware ESP32, y que existe evidencia suficiente para documentar funcionamiento, limitaciones y repetibilidad.

## Matriz de pruebas

| ID | Prueba | Subsistema | Evidencia esperada | Estado |
|---|---|---|---|---|
| VAL-001 | Compilación ESP-IDF J1-J5 | Firmware | Registro de compilación local | Completado localmente |
| VAL-002 | Compilación ROS 2 `can_comm_pkg` | Software | `colcon build` exitoso | Completado localmente |
| VAL-003 | Inicio de `can_node` con `vcan` | ROS 2 / CAN | Log de nodo iniciado | Completado localmente |
| VAL-004 | Teleoperación por teclado | ROS 2 / CAN | Video y notas de prueba | Evidencia bruta identificada |
| VAL-005 | J5 rampa 100 mm, 5 repeticiones | Elevador | Video y tabla resumen | Evidencia bruta identificada |
| VAL-006 | J5 trapezoidal 100 mm, 5 repeticiones | Elevador | Video y tabla resumen | Evidencia bruta identificada |
| VAL-007 | Bus CAN físico | Electrónica | `candump` y respuesta de nodos | Pendiente con hardware |
| VAL-008 | Pick-and-place integrado | Sistema completo | Video, tiempo de ciclo y éxito/falla | Pendiente |
| VAL-009 | Percepción / lectura | Visión | Logs, aciertos y tiempos | Pendiente |
| VAL-010 | Cinemática | Modelo del robot | Tabla de objetivo vs medición | Pendiente |

## Criterios mínimos por prueba

Cada prueba debe incluir:

- identificador de prueba;
- objetivo;
- subsistema evaluado;
- configuración usada;
- comando o procedimiento;
- evidencia obtenida;
- resultado observado;
- limitaciones o incidencias.

## Criterios de publicación

Para el artículo no es necesario presentar todas las pruebas como si fueran ensayos certificados. Sí es necesario que cada evidencia sea trazable y que el lector pueda entender qué se probó, cómo se probó y qué resultado se obtuvo.

## Prioridad inmediata

1. Registrar videos existentes en `validation/media/media_index.md`.
2. Crear tablas resumen para J5 rampa y trapezoidal.
3. Probar entry points ROS 2 adicionales.
4. Preparar figuras comparativas para `validation/figures/`.
5. Documentar pruebas físicas CAN cuando los ESP32 estén disponibles.

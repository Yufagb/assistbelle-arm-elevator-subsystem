# Pruebas de movimiento articular

Esta carpeta contiene las pruebas curadas de movimiento de articulaciones y del elevador J5.

## Objetivo

Documentar el comportamiento de los actuadores ante comandos reproducibles desde ROS 2/CAN. Para publicación, se debe conservar una tabla resumen, evidencia audiovisual y, cuando existan datos numéricos, archivos CSV con posición, referencia, error y tiempo.

## Organización recomendada

```text
joint_motion_tests/
├── j5_motion_summary.csv
├── j5_motion_notes.md
├── step/
├── ramp/
├── trapezoidal/
├── plots/
└── summary_tables/
```

## Evidencias identificadas

| Prueba | Evidencia asociada | Descripción | Estado |
|---|---|---|---|
| J5 rampa 100 mm, 5 repeticiones | `validation/media/j5_ramp_100mm_5reps.mp4` | Movimiento del elevador con perfil rampa. | Pendiente de copiar o enlazar. |
| J5 trapezoidal 100 mm, 5 repeticiones | `validation/media/j5_trapezoidal_100mm_5reps.mp4` | Movimiento del elevador con perfil trapezoidal. | Pendiente de copiar o enlazar. |
| Teleoperación por teclado | `validation/media/teleop_keyboard_test.mp4` | Movimiento comandado por interfaz de teclado. | Pendiente de copiar o enlazar. |

## Campos mínimos para datos CSV

Cuando existan datos numéricos, usar columnas como:

| Columna | Descripción |
|---|---|
| `time_s` | Tiempo en segundos. |
| `joint_id` | Identificador de articulación o eje. |
| `profile` | Perfil usado: step, ramp, trapezoidal. |
| `target_position` | Posición de referencia. |
| `measured_position` | Posición medida o estimada. |
| `error` | Diferencia entre referencia y medición. |
| `command_id` | ID CAN usado para el comando. |
| `notes` | Observaciones relevantes. |

## Criterio de comparación

Para HardwareX no es obligatorio demostrar una nueva teoría de control. Lo importante es mostrar que el hardware puede reproducir movimientos controlados y que el sistema cuenta con evidencia clara de funcionamiento.

Indicadores útiles:

- repetibilidad cualitativa del movimiento;
- estabilidad del perfil trapezoidal;
- ausencia de fallas visibles durante la secuencia;
- relación entre comando ROS 2/CAN y movimiento observado;
- descripción clara del perfil usado y del desplazamiento objetivo.

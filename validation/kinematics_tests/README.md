# Pruebas de cinemática

Esta carpeta contiene la validación de cinemática directa e inversa del manipulador.

## Objetivo

Comparar posiciones objetivo, valores articulares calculados y posiciones observadas del efector final. Esta validación permite justificar que el modelo cinemático usado por ROS 2 es coherente con el comportamiento físico del prototipo.

## Organización recomendada

```text
kinematics_tests/
├── kinematics_summary.csv
├── notes.md
├── raw_data/
├── processed_data/
└── plots/
```

## Campos mínimos para `kinematics_summary.csv`

| Campo | Descripción |
|---|---|
| `test_id` | Identificador de prueba. |
| `target_x` | Coordenada X objetivo. |
| `target_y` | Coordenada Y objetivo. |
| `target_z` | Coordenada Z objetivo. |
| `q1` a `q5` | Valores articulares calculados o comandados. |
| `measured_x` | Coordenada X medida, si existe. |
| `measured_y` | Coordenada Y medida, si existe. |
| `measured_z` | Coordenada Z medida, si existe. |
| `error_mm` | Error euclidiano o error principal. |
| `notes` | Observaciones. |

## Evidencia aceptable

Se puede usar cualquiera de estas fuentes:

- mediciones manuales del efector final;
- datos exportados desde ROS 2;
- capturas o datos de Tracker;
- logs de comandos articulares;
- comparación cualitativa si no hay medición precisa disponible.

## Estado actual

Pendiente de cargar datos curados. El modelo y los comandos asociados deben relacionarse con `ros2_ws/` y con las especificaciones del robot en `docs/ESPECIFICACIONES_ROBOT.md`, si ese documento está disponible en la rama.

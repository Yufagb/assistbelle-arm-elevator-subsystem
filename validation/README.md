# Validación

Esta carpeta contiene las evidencias curadas de validación del robot para la preparación del paquete HardwareX.

La validación debe separar los datos brutos de los datos seleccionados para publicación. Los archivos originales pueden permanecer en `resultados/`, pero las evidencias limpias, renombradas y descritas deben colocarse en `validation/`.

## Objetivo

Documentar que el sistema puede ejecutar pruebas reproducibles de movimiento, comunicación CAN, control desde ROS 2 y operación integrada.

## Subcarpetas

| Carpeta | Contenido esperado |
|---|---|
| `joint_motion_tests/` | Pruebas de articulaciones y elevador: escalón, rampa, trapezoidal y comparaciones. |
| `kinematics_tests/` | Validación de cinemática directa e inversa. |
| `perception_tests/` | Pruebas de visión, lectura de códigos o identificación de objetos. |
| `pick_and_place_tests/` | Pruebas integradas de manipulación. |
| `figures/` | Gráficas finales listas para paper. |
| `media/` | Videos, capturas y enlaces a evidencias audiovisuales. |

## Evidencias actuales identificadas

| Evidencia bruta | Destino recomendado | Tipo de prueba |
|---|---|---|
| `resultados/Teclado_P1.mp4` | `validation/media/teleop_keyboard_test.mp4` | Teleoperación por teclado. |
| `resultados/j5_ramp_100.0mm_5reps.mp4` | `validation/media/j5_ramp_100mm_5reps.mp4` | Elevador J5 con perfil rampa. |
| `resultados/j5_trap_100.0mm_5reps.mp4` | `validation/media/j5_trapezoidal_100mm_5reps.mp4` | Elevador J5 con perfil trapezoidal. |

## Criterio para aceptar una evidencia

Cada evidencia debe tener:

- nombre de archivo claro;
- tipo de prueba;
- fecha o versión del sistema, si está disponible;
- descripción breve;
- parámetros principales de la prueba;
- resultado observado;
- relación con firmware, ROS 2 o hardware probado.

## Comandos sugeridos para mover evidencias locales

```bash
cd ~/robot-project

mkdir -p validation/media

cp "resultados/Teclado_P1.mp4" "validation/media/teleop_keyboard_test.mp4"
cp "resultados/j5_ramp_100.0mm_5reps.mp4" "validation/media/j5_ramp_100mm_5reps.mp4"
cp "resultados/j5_trap_100.0mm_5reps.mp4" "validation/media/j5_trapezoidal_100mm_5reps.mp4"
```

Si los videos son muy pesados, se recomienda no versionarlos directamente en GitHub. En ese caso, subirlos a almacenamiento externo y registrar los enlaces en `validation/media/media_index.md`.

## Orden recomendado de trabajo

1. Registrar videos en `validation/media/media_index.md`.
2. Mover o enlazar evidencias seleccionadas.
3. Crear tablas resumen en `joint_motion_tests/` y `pick_and_place_tests/`.
4. Generar figuras finales en `validation/figures/`.
5. Referenciar los resultados desde el manuscrito en `paper/`.

# Índice de media de validación

Este archivo registra videos, capturas o enlaces audiovisuales usados como evidencia de validación.

## Evidencias locales identificadas

| ID | Archivo recomendado | Fuente original | Tipo de prueba | Subsistema | Descripción | Estado |
|---|---|---|---|---|---|---|
| MED-001 | `teleop_keyboard_test.mp4` | `resultados/Teclado_P1.mp4` | Teleoperación | ROS 2 + CAN | Prueba de movimiento comandado por teclado. | Pendiente de copiar o enlazar. |
| MED-002 | `j5_ramp_100mm_5reps.mp4` | `resultados/j5_ramp_100.0mm_5reps.mp4` | Movimiento articular | Elevador J5 | Prueba del eje prismático con perfil rampa de 100 mm y 5 repeticiones. | Pendiente de copiar o enlazar. |
| MED-003 | `j5_trapezoidal_100mm_5reps.mp4` | `resultados/j5_trap_100.0mm_5reps.mp4` | Movimiento articular | Elevador J5 | Prueba del eje prismático con perfil trapezoidal de 100 mm y 5 repeticiones. | Pendiente de copiar o enlazar. |

## Criterios de selección

Una evidencia audiovisual se considera útil para publicación si permite verificar al menos uno de estos puntos:

- ejecución de un comando desde ROS 2;
- respuesta de una articulación o del elevador;
- comparación entre perfiles de movimiento;
- funcionamiento del bus CAN;
- funcionamiento integrado del robot;
- manipulación de un objeto o tarea representativa.

## Recomendación de almacenamiento

Si los videos pesan poco, pueden colocarse directamente en `validation/media/`. Si pesan mucho, deben alojarse externamente y registrarse aquí con un enlace estable.

## Comandos locales sugeridos

```bash
cd ~/robot-project

mkdir -p validation/media

cp "resultados/Teclado_P1.mp4" "validation/media/teleop_keyboard_test.mp4"
cp "resultados/j5_ramp_100.0mm_5reps.mp4" "validation/media/j5_ramp_100mm_5reps.mp4"
cp "resultados/j5_trap_100.0mm_5reps.mp4" "validation/media/j5_trapezoidal_100mm_5reps.mp4"
```

Antes de subir videos al repositorio, revisar su tamaño:

```bash
ls -lh validation/media/*.mp4
```

Si algun video supera un tamaño razonable para GitHub, mantener solo el índice y subir el archivo a un almacenamiento externo.

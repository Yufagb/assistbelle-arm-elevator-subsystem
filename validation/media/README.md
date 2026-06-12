# Media de validación

Esta carpeta contiene videos, capturas o enlaces audiovisuales usados como evidencia de validación.

## Archivo índice

El archivo principal de esta carpeta es:

```text
media_index.md
```

Ese índice registra cada evidencia con:

- ID de evidencia;
- nombre recomendado del archivo;
- fuente original;
- tipo de prueba;
- subsistema evaluado;
- descripción;
- estado.

## Evidencias previstas

| Archivo recomendado | Prueba | Subsistema |
|---|---|---|
| `teleop_keyboard_test.mp4` | Teleoperación por teclado | ROS 2 + CAN |
| `j5_ramp_100mm_5reps.mp4` | Movimiento con perfil rampa | Elevador J5 |
| `j5_trapezoidal_100mm_5reps.mp4` | Movimiento con perfil trapezoidal | Elevador J5 |

## Política de almacenamiento

Si los videos son pequeños, pueden versionarse directamente en esta carpeta.

Si los videos son pesados, no deben subirse directamente a GitHub. En ese caso, se debe usar almacenamiento externo estable y colocar el enlace en `media_index.md`.

## Comandos locales sugeridos

```bash
cd ~/robot-project
mkdir -p validation/media

cp "resultados/Teclado_P1.mp4" "validation/media/teleop_keyboard_test.mp4"
cp "resultados/j5_ramp_100.0mm_5reps.mp4" "validation/media/j5_ramp_100mm_5reps.mp4"
cp "resultados/j5_trap_100.0mm_5reps.mp4" "validation/media/j5_trapezoidal_100mm_5reps.mp4"

ls -lh validation/media/*.mp4
```

## Criterio para uso en paper

Un video debe usarse en el paper o repositorio final solo si:

- muestra claramente el subsistema evaluado;
- tiene nombre trazable;
- está descrito en `media_index.md`;
- no contiene información irrelevante o sensible;
- se relaciona con una prueba descrita en `validation/validation_plan.md`.

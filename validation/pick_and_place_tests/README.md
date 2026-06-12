# Pruebas pick-and-place

Esta carpeta contiene las pruebas de manipulación integrada del robot.

## Objetivo

Registrar si el sistema puede ejecutar una tarea completa de tomar, trasladar y soltar un objeto o implemento dentro de un entorno controlado.

## Organización recomendada

```text
pick_and_place_tests/
├── pick_and_place_summary.csv
├── notes.md
├── raw_data/
├── processed_data/
└── plots/
```

## Campos mínimos para la tabla resumen

| Campo | Descripción |
|---|---|
| `test_id` | Identificador único de prueba. |
| `object` | Objeto manipulado. |
| `start_pose` | Posición inicial del objeto o efector. |
| `target_pose` | Posición final esperada. |
| `success` | Resultado: success / fail / partial. |
| `cycle_time_s` | Tiempo total del ciclo, si fue medido. |
| `media_file` | Video o imagen asociada. |
| `notes` | Observaciones de falla, vibración, retraso o intervención humana. |

## Criterio de éxito

Una prueba puede considerarse exitosa si:

- el robot llega a la zona de toma;
- el gripper cierra o interactúa con el objeto;
- el objeto se traslada hacia la zona objetivo;
- el objeto se libera o posiciona de forma controlada;
- no ocurre una parada no planificada ni pérdida visible de control.

## Estado actual

No hay una evidencia pick-and-place curada en esta carpeta. Si existe video bruto en `resultados/`, debe copiarse o enlazarse desde `validation/media/` y describirse en una tabla resumen.

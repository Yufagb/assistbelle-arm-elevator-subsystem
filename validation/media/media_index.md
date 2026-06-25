# Índice de media de validación

Este archivo registra videos, capturas o enlaces audiovisuales usados como evidencia de validación.

## Videos representativos versionados

| ID | Archivo | Tipo de prueba | Subsistema | Descripción | Estado |
|---|---|---|---|---|---|
| MED-001 | `validation/media/joint_motion/j5_ramp_100.0mm_5reps_robot.mp4` | Movimiento articular | Elevador J5 | Perfil rampa de 100 mm con 5 repeticiones, vista del robot. | Subido con Git LFS. |
| MED-002 | `validation/media/joint_motion/j5_trap_100.0mm_5reps_robot.mp4` | Movimiento articular | Elevador J5 | Perfil trapezoidal de 100 mm con 5 repeticiones, vista del robot. | Subido con Git LFS. |
| MED-003 | `validation/media/joint_motion/j1_step_30.0deg_5reps_robot.mp4` | Movimiento articular | J1 | Perfil escalón de 30 grados con 5 repeticiones, vista del robot. | Subido con Git LFS. |
| MED-004 | `validation/media/perception/resultado_percepcion_video_prueba_completa.mp4` | Percepción | Visión | Video de prueba completa de percepción. | Subido con Git LFS. |
| MED-005 | `validation/media/teleoperation/Teclado_P2.mp4` | Teleoperación | ROS 2 + CAN | Prueba de movimiento comandado por teclado. | Subido con Git LFS. |

## Videos locales no versionados

Los demás videos de `validation/media/` se mantienen como evidencia local no versionada para evitar subir todo el conjunto audiovisual. Pueden subirse en una versión posterior o enlazarse externamente si se requiere reproducibilidad audiovisual completa.

| Grupo local | Estado |
|---|---|
| `validation/media/joint_motion/` | Solo se versionó un subconjunto representativo. |
| `validation/media/kinematics/` | Pendiente de selección o enlace externo. |
| `validation/media/teleoperation/` | Solo se versionó `Teclado_P2.mp4`. |
| `validation/media/perception/` | Se versionó el video de percepción principal. |

## Criterios de selección

Una evidencia audiovisual se considera útil para publicación si permite verificar al menos uno de estos puntos:

- ejecución de un comando desde ROS 2;
- respuesta de una articulación o del elevador;
- comparación entre perfiles de movimiento;
- funcionamiento del bus CAN;
- funcionamiento integrado del robot;
- manipulación de un objeto o tarea representativa.

## Recomendación de almacenamiento

Si se requiere conservar el conjunto audiovisual completo, se recomienda alojarlo en almacenamiento externo estable y registrar aquí el enlace. Para el repositorio HardwareX se prioriza un subconjunto representativo con Git LFS.

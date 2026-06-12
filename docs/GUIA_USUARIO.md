# Guía de Usuario

## 🎮 Teleoperación

Controla el robot usando el teclado.

```bash
ros2 run can_comm_pkg control_teclado
```

*   **Teclas**:
    *   `1`/`Q`: J1 +/-
    *   `2`/`W`: J2 +/-
    *   `3`/`E`: J3 +/-
    *   `4`/`R`: J4 +/-
    *   `5`/`T`: J5 +/-

## 📈 Generación de Trayectorias

Lanza la GUI para diseñar y ejecutar trayectorias.

```bash
ros2 run can_comm_pkg can_traj
```

1.  **Home**: Mueve el robot a la posición cero.
2.  **Add Point**: Añade la configuración actual a la trayectoria.
3.  **Generate**: Crea un camino suave (LSPB/Trapezoidal).
4.  **Execute**: Envía comandos al robot.

## 🧪 Pruebas de Rendimiento

Ejecuta pruebas automatizadas para verificar el rendimiento de las articulaciones.

**Sintaxis:**
```bash
ros2 run can_comm_pkg j<ARTICULACION>_<PERFIL>
```

**Pruebas Disponibles:**
*   **Articulaciones**: `j1`, `j2`, `j3`, `j4`, `j5`
*   **Perfiles**: `step` (escalón), `ramp` (rampa), `trap` (trapezoidal)

**Ejemplo:**
```bash
ros2 run can_comm_pkg j5_step
```
*   Solicita Objetivo (mm) y Tiempo.
*   Ejecuta 5 repeticiones.
*   Guarda datos y gráficos en `resultados/`.

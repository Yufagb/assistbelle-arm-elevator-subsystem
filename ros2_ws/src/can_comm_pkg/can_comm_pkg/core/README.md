# Core del Paquete CAN

Esta carpeta contiene la lógica central para la comunicación de bajo nivel con el robot a través del bus CAN.

## Archivos Principales

### `can_node.py`
Es el Nodo ROS 2 principal (`can_node`). Actúa como puente entre ROS 2 y el hardware CAN.

*   **Suscripciones**:
    *   `/can_command` (`std_msgs/String`): Recibe comandos de alto nivel (ej. "C1:1.57,0.5").
*   **Publicaciones**:
    *   `/motors_state` (`Float32MultiArray`): Estado crudo de los motores [pos, vel].
    *   `/joint_states` (`JointState`): Estado del robot compatible con Rviz.
*   **Frecuencia**:
    *   Bucle de recepción: 100 Hz.
    *   Publicación inmediata al recibir feedback (0xB) para minimizar latencia.

### `driver.py`
Clase `CANDriver` que envuelve la librería `python-can`. Maneja la creación del socket CAN (`can0`) y el envío/recepción de bytes crudos.

### `message.py`
Clase `CANMessage` que define la estructura de una trama CAN (ID, DLC, Payload).

## Uso

Este nodo se ejecuta automáticamente al lanzar el sistema, pero puede correrse aisladamente para pruebas:

```bash
ros2 run can_comm_pkg can_node
```

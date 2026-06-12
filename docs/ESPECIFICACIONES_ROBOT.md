# Especificaciones del Robot

## 🦾 Límites de Articulaciones

El robot consiste en una base prismática (J5/Ascensor) y un brazo articulado de 4 grados de libertad (J1-J4).

| Articulación | Tipo | Nombre | Límite Min | Límite Max | Unidad |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | Revoluta | Base | -135° | +34° | Grados |
| **J2** | Revoluta | Hombro | -45° | +70° | Grados |
| **J3** | Revoluta | Codo | -140° | +120° | Grados |
| **J4** | Revoluta | Muñeca | -180° | +180° | Grados |
| **J5** | Prismática | Ascensor | 0 mm | 350 mm | Milímetros |

> **Nota**: J5 es físicamente el ascensor base, pero a menudo se direcciona como índice 5 o 0 en diferentes contextos. En el protocolo CAN, es el Motor 5.

## 📐 Parámetros Denavit-Hartenberg (DH)

La cadena cinemática se define de la siguiente manera:

| Eslabón | $\theta$ (Offset) | $d$ (m) | $a$ (m) | $\alpha$ (rad) |
| :--- | :--- | :--- | :--- | :--- |
| **0 (Ascensor)** | 0 | $d_0 + 0.4$ | 0 | 0 |
| **1 (Base)** | $\theta_1 + 360^\circ$ | 0 | 0 | -90° |
| **2 (Fijo)** | $180^\circ$ | 0.1 | 0 | 0 |
| **3 (Hombro)** | $\theta_2 + 180^\circ$ | 0 | 0.215 | 0 |
| **4 (Codo)** | $\theta_3$ | 0 | 0.25 | 180° |
| **5 (Muñeca)** | $\theta_4$ | 0 | 0.125 | 90° |

## 🔌 Interfaz de Hardware

*   **Bus**: CAN Bus (Controller Area Network)
*   **Bitrate**: 1 Mbps (típico)
*   **Interfaz**: `can0` (SocketCAN)
*   **Motores**: Actuadores personalizados con controladores integrados.

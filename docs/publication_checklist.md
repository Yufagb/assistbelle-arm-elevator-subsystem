# Checklist temporal de publicación

Este archivo es temporal. Sirve para saber qué falta antes de enviar el artículo. Cuando todo esté completo, se puede borrar o mover a una carpeta interna.

Leyenda:

- [x] hecho
- [ ] pendiente
- [~] parcial

## 1. Organización del repositorio

- [x] Crear rama basada en la versión actual de main.
- [x] Mantener documentación y código existente de main.
- [x] Agregar README principal orientado a publicación.
- [x] Crear estructura de carpetas para hardware, electrónica, firmware, validación y paper.
- [x] Agregar descripciones en carpetas vacías mediante README.md.
- [x] Mejorar .gitignore.
- [ ] Quitar archivos generados que ya estén versionados: build, install, log, .idea.
- [ ] Decidir si se publicará este repo o si se copiará a un repo limpio final.

## 2. Licencias y citación

- [ ] Agregar licencia completa para software y firmware.
- [ ] Agregar licencia completa para hardware y CAD.
- [ ] Agregar licencia completa para documentación y figuras.
- [ ] Agregar CITATION.cff.
- [ ] Indicar licencias por carpeta.

## 3. Mecánica

- [ ] Subir CAD editable.
- [ ] Subir archivos STEP.
- [ ] Subir archivos STL.
- [ ] Subir planos con dimensiones.
- [ ] Subir fotos del brazo armado.
- [ ] Subir fotos del elevador.
- [ ] Subir fotos del gripper.
- [ ] Completar lista de tornillos, tuercas, rodamientos y perfiles.

## 4. Electrónica

- [ ] Subir diagrama general de cableado.
- [ ] Subir diagrama CAN.
- [ ] Subir diagrama de distribución de potencia.
- [ ] Subir tabla de pines ESP32.
- [ ] Subir tabla de drivers de motor.
- [ ] Subir fotos del cableado y tablero.

## 5. Firmware

- [~] Existe documentación inicial en Codigo_esp32.
- [ ] Descomprimir el ZIP de firmware.
- [ ] Separar firmware por nodo.
- [ ] Agregar instrucciones de compilación.
- [ ] Agregar instrucciones de carga al ESP32.
- [ ] Documentar IDs de nodos CAN.
- [ ] Documentar límites de seguridad configurados en firmware.

## 6. Software ROS 2

- [x] Workspace ROS 2 existente.
- [x] Paquete can_comm_pkg existente.
- [x] Nodo CAN existente.
- [x] Scripts de teleoperación existentes.
- [x] Scripts de pruebas existentes.
- [x] Script de identificación de productos existente.
- [ ] Verificar que todos los entry points compilen.
- [ ] Agregar comandos SocketCAN.
- [ ] Aclarar si product_identifier.py es standalone o nodo ROS 2.
- [ ] Agregar instalación de dependencias de visión.

## 7. BOM

- [ ] Completar modelos exactos.
- [ ] Completar cantidades.
- [ ] Completar proveedores.
- [ ] Completar costos.
- [ ] Completar moneda.
- [ ] Agregar alternativas de compra.
- [ ] Calcular costo total.

## 8. Manuales

- [ ] Completar manual de ensamblaje.
- [ ] Completar manual de operación.
- [ ] Completar manual de calibración.
- [ ] Completar notas de seguridad.
- [ ] Agregar troubleshooting.
- [ ] Agregar checklist de preoperación.

## 9. Validación

- [ ] Curar CSV de pruebas articulares.
- [ ] Curar gráficos finales.
- [ ] Curar datos de cinemática.
- [ ] Curar datos de percepción.
- [ ] Curar datos de pick-and-place.
- [ ] Agregar videos o enlaces externos.
- [ ] Agregar índice de dataset.

## 10. Manuscrito

- [ ] Crear borrador del manuscrito.
- [ ] Agregar figuras finales.
- [ ] Agregar tablas finales.
- [ ] Agregar referencias.
- [ ] Agregar highlights.
- [ ] Agregar statement de disponibilidad de datos.

## 11. Limpieza final

- [ ] Reemplazar placeholders.
- [ ] Reemplazar correos de ejemplo en package.xml y setup.py.
- [ ] Revisar enlaces del README.
- [ ] Verificar acceso público o enlace de archivo.
- [ ] Quitar este checklist temporal.

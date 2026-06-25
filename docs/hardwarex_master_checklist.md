# Checklist maestro HardwareX

Checklist maestro para preparar el repositorio como paquete reproducible.

Leyenda:

- `[x]` completado
- `[~]` parcial
- `[ ]` pendiente
- `[d]` diferido por falta de acceso físico al prototipo o por congelamiento final pendiente

## Índice

- [A. Identidad del hardware](#a-identidad-del-hardware)
- [B. Archivos mecánicos](#b-archivos-mecánicos)
- [C. Electrónica](#c-electrónica)
- [D. Firmware](#d-firmware)
- [E. ROS 2 y software](#e-ros-2-y-software)
- [F. Datos de validación](#f-datos-de-validación)
- [G. Manuscrito](#g-manuscrito)
- [H. Limpieza final](#h-limpieza-final)

## A. Identidad del hardware

- [x] Nombre de trabajo definido: Assistbelle / Robot asistivo 5-DOF.
- [x] Título tentativo del artículo definido.
- [x] Alcance limitado a laboratorio o entorno controlado.
- [ ] Nombre final del hardware confirmado.
- [ ] Resumen final del uso previsto.
- [ ] Limitaciones finales del prototipo declaradas.

## B. Archivos mecánicos

- [x] CAD completo del sistema elevador cargado: `hardware/cad/complete_robot/ASM_Elevator_System_v60.f3z`.
- [~] CAD completo del robot/brazo: fuera del cierre actual del paquete elevador v60 o pendiente de congelar según alcance final.
- [x] CAD del elevador cargado como snapshot de trabajo v60.
- [~] CAD del brazo: pendiente si el release final incluye brazo completo en este repositorio.
- [~] CAD del gripper: pendiente si el release final incluye gripper completo en este repositorio.
- [x] CAD de soportes y adaptadores principales del elevador incluido dentro del ensamblaje v60.
- [x] STEP completo cargado: `hardware/step/ASM_Elevator_System_v60.step`.
- [d] STEP por subconjunto: opcional para snapshot v60; agregar antes de congelar release final si se requiere mayor navegabilidad.
- [x] STL de piezas imprimibles/fabricadas cargado para las piezas identificadas en BOM v60.
- [x] Planos con dimensiones cargados para base plate, top plate y gantry plate.
- [x] DXF de fabricación cargado para top plate y gantry plate.
- [~] Tabla de tornillos, rodamientos, perfiles y piezas estándar documentada en BOM/fasteners; falta verificación física final.
- [d] Fotos del prototipo diferidas por falta de acceso físico al robot.

## C. Electrónica

- [x] Pinouts por nodo documentados.
- [x] Raspberry Pi a MCP2515 documentado.
- [x] Bus principal documentado parcialmente.
- [x] Driver por articulación documentado parcialmente.
- [x] Carpeta de esquemáticos creada.
- [x] Índice de esquemáticos creado.
- [ ] Confirmar que los esquemáticos cubren sistema general, CAN, potencia y drivers.
- [ ] Exportar esquemáticos a PDF/PNG si solo están en formato editable.
- [ ] Diagrama CAN final revisado.
- [ ] Diagrama de potencia final revisado.
- [ ] Tabla de conectores finales.
- [ ] Fotos o imágenes reales de electrónica.

## D. Firmware

- [x] Firmware migrado a `firmware/`.
- [x] Proyectos ESP-IDF J1-J4 agregados.
- [x] Proyecto ESP-IDF J5/TB6600 agregado.
- [x] Proyecto compilable localmente para J1-J5.
- [x] Instrucciones de carga documentadas.
- [x] IDs CAN documentados.
- [x] Parámetros de control documentados parcialmente.
- [ ] Límites de seguridad finales documentados.
- [ ] Confirmar formato final de payload CAN contra ROS 2.

## E. ROS 2 y software

- [x] Código ROS 2 mantenido dentro de `ros2_ws/`.
- [x] Guía de entry points creada.
- [x] Comandos SocketCAN documentados.
- [ ] Compilación reproducible validada desde clon limpio.
- [ ] Entry points verificados uno por uno.
- [ ] Dependencias Python verificadas.
- [ ] Script de visión definido claramente como nodo ROS o standalone.

## F. Datos de validación

- [x] Plan de validación creado.
- [x] Índice de media creado.
- [x] Tabla inicial J5 creada.
- [ ] Pruebas articulares curadas.
- [ ] Pruebas de cinemática curadas.
- [ ] Pruebas de percepción curadas.
- [ ] Pruebas pick-and-place curadas.
- [ ] Figuras finales listas.
- [ ] Videos o enlaces listos.
- [ ] Índice de dataset final listo.

## G. Manuscrito

- [ ] Tabla de especificaciones.
- [ ] Contexto del hardware.
- [ ] Descripción del hardware.
- [ ] Resumen de archivos de diseño.
- [ ] Resumen de lista de materiales.
- [ ] Instrucciones de construcción.
- [ ] Instrucciones de operación.
- [ ] Validación y caracterización.
- [ ] Notas de seguridad.
- [ ] Referencias.

## H. Limpieza final

- [x] `.gitignore` reforzado para ROS 2 y ESP-IDF.
- [x] `.gitattributes` configurado para Git LFS en CAD, STEP, STL, DXF y media pesada.
- [x] `LICENSE` creado.
- [x] `CITATION.cff` creado.
- [ ] Verificar que no queden artefactos versionados en `build`, `install`, `log`, `.vscode` o `.idea`.
- [ ] Reemplazar placeholders.
- [ ] Revisar enlaces internos.
- [ ] Revisar accesibilidad del repositorio.
- [ ] Eliminar o archivar checklists temporales.

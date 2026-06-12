# Checklist maestro HardwareX

Checklist maestro para preparar el repositorio como paquete reproducible.

## A. Identidad del hardware

- [x] Nombre de trabajo del hardware definido: Assistbelle / Robot 5-DOF.
- [x] Titulo tentativo del articulo definido.
- [x] Alcance limitado a laboratorio o entorno controlado.
- [ ] Nombre final del hardware confirmado.
- [ ] Resumen final del uso previsto.
- [ ] Limitaciones finales del prototipo declaradas.

## B. Archivos mecanicos

- [ ] CAD completo del robot.
- [ ] CAD del brazo.
- [ ] CAD del elevador.
- [ ] CAD del gripper.
- [ ] CAD de soportes y adaptadores.
- [ ] STEP completo.
- [ ] STEP por subconjunto.
- [ ] STL de piezas imprimibles.
- [ ] Planos con dimensiones.
- [ ] Tabla de tornillos, rodamientos, perfiles y piezas estandar.
- [ ] Fotos del prototipo.

## C. Electronica

- [x] Pinouts por nodo documentados.
- [x] Raspberry Pi a MCP2515 documentado.
- [x] Bus principal documentado parcialmente.
- [x] Driver por articulacion documentado parcialmente.
- [ ] Diagrama general final en imagen/PDF/KiCad.
- [ ] Diagrama CAN final.
- [ ] Diagrama de potencia final.
- [ ] Tabla de conectores finales.
- [ ] Fotos o imagenes de electronica.

## D. Firmware

- [x] Firmware descomprimido y migrado a `firmware/`.
- [x] Proyectos ESP-IDF J1-J4 agregados.
- [x] Proyecto ESP-IDF J5/TB6600 agregado.
- [x] Proyecto compilable localmente para J1-J5.
- [x] Instrucciones de carga documentadas.
- [x] IDs CAN documentados.
- [x] Parametros de control documentados parcialmente.
- [ ] Limites de seguridad finales documentados.
- [ ] Confirmar formato final de payload CAN contra ROS 2.

## E. ROS 2 y software

- [x] Codigo ROS 2 mantenido dentro de `ros2_ws/`.
- [ ] Compilacion reproducible validada despues de limpieza.
- [ ] Comandos de instalacion finalizados.
- [ ] Comandos SocketCAN finalizados.
- [ ] Entry points verificados.
- [ ] Dependencias Python verificadas.
- [ ] Script de vision definido claramente como nodo ROS o standalone.

## F. Datos de validacion

- [ ] Pruebas articulares curadas.
- [ ] Pruebas de cinematica curadas.
- [ ] Pruebas de percepcion curadas.
- [ ] Pruebas pick-and-place curadas.
- [ ] Figuras finales listas.
- [ ] Videos o enlaces listos.
- [ ] Indice de dataset listo.

## G. Manuscrito

- [ ] Tabla de especificaciones.
- [ ] Contexto del hardware.
- [ ] Descripcion del hardware.
- [ ] Resumen de archivos de diseno.
- [ ] Resumen de lista de materiales.
- [ ] Instrucciones de construccion.
- [ ] Instrucciones de operacion.
- [ ] Validacion y caracterizacion.
- [ ] Notas de seguridad.
- [ ] Referencias.

## H. Limpieza final

- [x] `.gitignore` reforzado para ROS 2 y ESP-IDF.
- [ ] Verificar que no queden artefactos versionados en `build`, `install`, `log`, `.vscode` o `.idea`.
- [ ] Reemplazar placeholders.
- [ ] Revisar enlaces internos.
- [ ] Revisar licencias.
- [ ] Revisar accesibilidad del repositorio.
- [ ] Eliminar o archivar checklists temporales.

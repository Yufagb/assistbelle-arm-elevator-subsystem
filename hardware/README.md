# Hardware

Paquete de diseno mecanico del manipulador robotico Assistbelle.

Esta carpeta debe contener solo archivos mecanicos necesarios para reproducir el robot. No colocar aqui codigo ROS 2, firmware ni datos de validacion.

## Estructura canonica

- cad: archivos CAD editables.
- step: exportaciones STEP neutrales.
- stl: archivos para impresion 3D.
- drawings: planos mecanicos con cotas.
- photos: fotos del sistema mecanico ensamblado.
- fasteners: tornillos, tuercas, rodamientos, perfiles y piezas mecanicas estandar.

## Subestructura CAD

- cad/complete_robot: ensamble completo.
- cad/arm: brazo de 4 GDL, articulaciones y eslabones.
- cad/elevator: mecanismo vertical de elevacion.
- cad/gripper: efector final o garra.
- cad/mounts: soportes, adaptadores y brackets.

## Carpetas antiguas

Las carpetas CAD_editable, STEP y STL fueron creadas en una pasada anterior. Para nuevos archivos usar solo las carpetas canonicas en minuscula: cad, step y stl.

## Requisito minimo para publicacion

Cada pieza mecanica personalizada debe tener al menos uno de estos elementos:

- archivo CAD editable
- exportacion STEP
- STL si es una pieza impresa en 3D
- plano con dimensiones
- foto mostrando la pieza instalada

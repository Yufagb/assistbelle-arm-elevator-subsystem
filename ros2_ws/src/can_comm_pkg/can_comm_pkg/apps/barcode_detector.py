#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class BarcodeDetector(Node):
    def __init__(self):
        super().__init__('barcode_detector')
        
        # Suscripción a la cámara (imagen comprimida)
        self.sub = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )
        
        # Publicador de imagen de debug
        self.pub_debug = self.create_publisher(
            CompressedImage,
            '/barcode_debug/compressed',
            10
        )
        
        self.get_logger().info("Barcode Detector iniciado. Esperando imágenes...")
        
        # Estado de Tracking
        self.last_roi = None # (x, y, w, h)
        self.frames_without_detection = 0
        self.MAX_FRAMES_LOST = 10

    def image_callback(self, msg):
        try:
            # 1. Convertir ROS CompressedImage -> OpenCV
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return

            # Lógica de Detección de Objetos (Candidatos)
            # Si NO estamos en tracking de código (Blue), buscamos candidatos (Yellow)
            candidate_roi = None # (x, y, w, h)
            
            if self.last_roi is None:
                # 1. Detección de Color (Botella Blanca)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Rango para objetos blancos/brillantes (baja saturación, alto valor)
                lower_white = np.array([0, 0, 160])
                upper_white = np.array([180, 60, 255])
                mask = cv2.inRange(hsv, lower_white, upper_white)
                
                # Limpieza morfológica de la máscara
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
                # Encontrar contornos
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                best_cnt = None
                max_area = 0
                
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    x, y, w, h = cv2.boundingRect(cnt)
                    aspect_ratio = float(h) / w
                    
                    # Filtros: Área mínima y forma vertical (botella)
                    if area > 3000 and aspect_ratio > 1.2:
                        if area > max_area:
                            max_area = area
                            best_cnt = cnt
                            candidate_roi = (x, y, w, h)
                
                if candidate_roi is not None:
                    cx, cy, cw, ch = candidate_roi
                    # Dibujar Candidato (Amarillo)
                    cv2.rectangle(frame, (cx, cy), (cx+cw, cy+ch), (0, 255, 255), 2)
                    cv2.putText(frame, "CANDIDATE", (cx, cy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            # Definir Área de Búsqueda para Código de Barras
            search_area = frame
            roi_offset_x, roi_offset_y = 0, 0
            
            if self.last_roi is not None:
                # MODO TRACKING (Azul) - Prioridad máxima
                x, y, w, h = self.last_roi
                margin = 50
                h_img, w_img = frame.shape[:2]
                x1 = max(0, x - margin); y1 = max(0, y - margin)
                x2 = min(w_img, x + w + margin); y2 = min(h_img, y + h + margin)
                search_area = frame[y1:y2, x1:x2]
                roi_offset_x, roi_offset_y = x1, y1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, "TRACKING", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
            elif candidate_roi is not None:
                # MODO CANDIDATO (Amarillo) - Buscamos código DENTRO de la botella
                x, y, w, h = candidate_roi
                # Recortamos un poco más adentro para evitar bordes ruidosos
                search_area = frame[y:y+h, x:x+w]
                roi_offset_x, roi_offset_y = x, y
            else:
                # MODO BÚSQUEDA GLOBAL - Si no hay nada, no procesamos código pesado
                # Opcional: procesar frame completo cada N frames para recuperar?
                # Por ahora, si no hay botella, no hay código. Ahorra CPU.
                search_area = None 

            if search_area is not None and search_area.size > 0:
                # Convertir a escala de grises (del área de búsqueda)
                gray = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)

                # Preprocesamiento avanzado v2 (Solo en el área de búsqueda)
                # 1. Upscaling
                scale_factor = 2.0
                width = int(gray.shape[1] * scale_factor)
                height = int(gray.shape[0] * scale_factor)
                resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)
                
                # 2. Reducción de Ruido
                blurred = cv2.GaussianBlur(resized, (5, 5), 0)
                
                # 3. Binarización Adaptativa
                thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 21, 10)
                                             
                # 4. Operaciones Morfológicas
                kernel_morph = np.ones((3, 3), np.uint8)
                morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_morph)
                
                # Intentamos detectar
                images_to_check = [
                    (gray, "Original Gray", 1.0),
                    (resized, "Resized", scale_factor),
                    (thresh, "Threshold", scale_factor),
                    (morph, "Morph", scale_factor)
                ]
                
                detections = []
                
                for img_check, name, current_scale in images_to_check:
                    objs = decode(img_check)
                    for obj in objs:
                        detections.append((obj, current_scale))

                # Procesar resultados
                if len(detections) > 0:
                    self.frames_without_detection = 0
                    best_obj, best_scale = detections[0]
                    
                    # Calcular ROI global para el siguiente frame (Tracking Azul)
                    inv_scale = 1.0 / best_scale
                    rect = best_obj.rect
                    
                    rx = int(rect.left * inv_scale)
                    ry = int(rect.top * inv_scale)
                    rw = int(rect.width * inv_scale)
                    rh = int(rect.height * inv_scale)
                    
                    gx = rx + roi_offset_x
                    gy = ry + roi_offset_y
                    
                    self.last_roi = (gx, gy, rw, rh)
                    
                else:
                    # Si estábamos en tracking azul y fallamos, contamos frames perdidos
                    if self.last_roi is not None:
                        self.frames_without_detection += 1
                        if self.frames_without_detection > self.MAX_FRAMES_LOST:
                            self.last_roi = None # Volver a buscar candidatos amarillos
                        
                # Visualización (Solo dibujamos si detectamos en este frame)
                seen_data = set()
                for obj, current_scale in detections:
                    data = obj.data.decode('utf-8')
                    if data in seen_data: continue
                    seen_data.add(data)
                    
                    inv_scale = 1.0 / current_scale
                    
                    # Mapear al frame GLOBAL
                    points = obj.polygon
                    pts_global = []
                    for p in points:
                        px = int(p.x * inv_scale) + roi_offset_x
                        py = int(p.y * inv_scale) + roi_offset_y
                        pts_global.append([px, py])
                    
                    if len(pts_global) == 4:
                        pts = np.array(pts_global, dtype=np.int32)
                        cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                    
                    # Centro Global
                    rect = obj.rect
                    cx = (rect.left + rect.width/2) * inv_scale + roi_offset_x
                    cy = (rect.top + rect.height/2) * inv_scale + roi_offset_y
                    
                    cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                    text = f"{data}"
                    cv2.putText(frame, text, (int(cx), int(cy) - 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    self.get_logger().info(f"Detectado: {data} | Centro: ({cx:.1f}, {cy:.1f})")

            # 4. Publicar imagen debug
            msg_debug = CompressedImage()
            msg_debug.header = msg.header
            msg_debug.format = "jpeg"
            msg_debug.data = np.array(cv2.imencode('.jpg', frame)[1]).tobytes()
            self.pub_debug.publish(msg_debug)

            # 5. Mostrar ventana local
            cv2.imshow("Barcode Detector - Main", frame)
            
            # Mostrar Morph (si estamos en ROI, será el recorte procesado)
            if search_area is not None and 'morph' in locals():
                display_morph = cv2.resize(morph, (400, 400)) # Tamaño fijo para ver
                cv2.imshow("Barcode Detector - Processed ROI", display_morph)
            
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error procesando imagen: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = BarcodeDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

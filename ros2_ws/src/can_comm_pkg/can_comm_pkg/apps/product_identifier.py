#!/usr/bin/env python3
import cv2
import time
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

# ================= CONFIGURATION =================
# Known Products Database
# Format: "BarcodeData": "ProductName"
PRODUCT_DB = {
    "817432015300": "Terbonova Full SPECTRUM",
    "0817432015300": "Terbonova Full SPECTRUM", # Possible EAN-13 padding
    "7750304005531": "Dexametasona 4 mg"
}

# Performance Thresholds (for visual feedback)
THRESH_D_MIN = 0.95
THRESH_FP_MAX = 0.02
THRESH_T_DET = 0.50
THRESH_S_ID = 0.97
THRESH_T_ID = 0.50

class PerformanceTracker:
    def __init__(self):
        self.total_frames = 0
        self.frames_with_detection = 0
        self.successful_identifications = 0
        self.false_positives = 0 # Detects something not in DB (assuming test env only has valid items)
        
        self.detection_times = []
        self.identification_times = []
        
        self.start_time = time.time()

    def update(self, detected, identified, t_det, t_id):
        self.total_frames += 1
        if detected:
            self.frames_with_detection += 1
            self.detection_times.append(t_det)
            
            if identified:
                self.successful_identifications += 1
                self.identification_times.append(t_id)
            else:
                # If detected but not identified, counts as FP for this specific closed-set scenario?
                # Or just "Unknown". Let's count "Unknown" as potential FP for the sake of the metric 
                # if the user implies only these 2 exist. 
                # However, strictly FP is detecting noise as a barcode.
                # We'll track "Unknowns" separately but for the metric FPmax, 
                # we'll use a heuristic: if confidence is low or format is weird (not applicable to pyzbar directly).
                # Let's assume any detection NOT in DB is a "False Positive" for this specific test.
                self.false_positives += 1 

    def get_metrics(self):
        # D: Detection Rate (approximate as % of frames with detection if we assume object is always present... 
        # actually we can't know if object is present. 
        # We will display "Detection Success" as (Frames with Detection / Total Frames) 
        # BUT this is only valid if the user holds the object in front all the time.
        # A better metric for the user to see is just the instantaneous times and the counters.
        
        d_rate = 0.0
        if self.total_frames > 0:
            d_rate = self.frames_with_detection / self.total_frames

        fp_rate = 0.0
        if self.total_frames > 0:
            fp_rate = self.false_positives / self.total_frames

        s_id = 0.0
        if self.frames_with_detection > 0:
            s_id = self.successful_identifications / self.frames_with_detection

        avg_t_det = np.mean(self.detection_times) if self.detection_times else 0.0
        avg_t_id = np.mean(self.identification_times) if self.identification_times else 0.0

        return d_rate, fp_rate, s_id, avg_t_det, avg_t_id

def main():
    # 1. Initialize Camera
    # 1. Initialize Camera
    # Prioritize external cameras (often start at index 2 on Linux)
    # 0 is usually the built-in laptop camera.
    camera_indices = [2, 4, 6, 8, 1, 0]
    cap = None
    
    for idx in camera_indices:
        print(f"Intentando abrir cámara en índice {idx}...")
        temp_cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if temp_cap.isOpened():
            # Optional: Check if it's actually returning frames
            ret, _ = temp_cap.read()
            if ret:
                cap = temp_cap
                print(f"Éxito: Cámara encontrada en índice {idx}")
                break
            else:
                temp_cap.release()
    
    if cap is None or not cap.isOpened():
        print("Error: No se encontró ninguna cámara funcional.")
        return

    # Optimize Camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # UI Constants
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    WINDOW_NAME = "Sistema de Identificacion de Productos"
    cv2.namedWindow(WINDOW_NAME)

    # --- CONFIGURACIÓN DE FOCO (SLIDER) ---
    def nothing(x): pass
    
    # Crear Trackbar para el foco
    # El rango suele ser 0-255, donde 0 es cerca y 255 lejos (o viceversa según driver)
    cv2.createTrackbar('Foco (0-255)', WINDOW_NAME, 0, 255, nothing)
    
    # Intentar desactivar autofocus una vez al inicio
    try:
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    except:
        pass
    
    tracker = PerformanceTracker()
    last_focus_val = -1

    while True:
        # Actualizar Foco desde Slider
        focus_val = cv2.getTrackbarPos('Foco (0-255)', WINDOW_NAME)
        if focus_val != last_focus_val:
            cap.set(cv2.CAP_PROP_FOCUS, focus_val)
            last_focus_val = focus_val

        ret, frame = cap.read()
        if not ret: break

        # Start Timer for Detection
        t0 = time.time()
        
        # Preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect
        decoded_objects = decode(gray)
        
        t_det = time.time() - t0
        
        detected = False
        identified = False
        t_id_val = 0.0
        product_name = "NINGUNO"
        
        # --- PROCESAMIENTO ---
        if decoded_objects:
            detected = True
            
            # Process the first/best detection
            obj = decoded_objects[0]
            barcode_data = obj.data.decode("utf-8")
            
            # Start Timer for Identification
            t1 = time.time()
            
            # Identification Logic
            product_name = PRODUCT_DB.get(barcode_data, "DESCONOCIDO")
            
            t_id_val = time.time() - t1
            
            if product_name != "DESCONOCIDO":
                identified = True
                color = (0, 255, 0) # Green
            else:
                color = (0, 0, 255) # Red
            
            # Draw Bounding Box & Label on Object
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                cv2.polylines(frame, [pts], True, color, 3)
            
            rect = obj.rect
            # Background for label
            cv2.rectangle(frame, (rect.left, rect.top - 30), (rect.left + rect.width, rect.top), color, -1)
            cv2.putText(frame, product_name, (rect.left + 5, rect.top - 8), 
                        FONT, 0.6, (0, 0, 0), 2)

        # Update Stats
        tracker.update(detected, identified, t_det, t_id_val)
        d_rate, fp_rate, s_id, avg_t_det, avg_t_id = tracker.get_metrics()

        # --- VISUALIZACIÓN (DASHBOARD) ---
        # Crear panel lateral derecho para estadísticas
        h, w = frame.shape[:2]
        panel_w = 280
        # Expandir imagen para el panel
        canvas = np.zeros((h, w + panel_w, 3), dtype=np.uint8)
        canvas[:, :w] = frame # Copiar imagen de cámara
        
        # Fondo del panel
        ui_bg_color = (50, 50, 50)
        canvas[:, w:] = ui_bg_color
        
        x_ui = w + 10
        y_ui = 30
        line_h = 25
        
        # Título
        cv2.putText(canvas, "ESTADISTICAS", (x_ui + 40, y_ui), FONT, 0.7, (255, 255, 255), 2)
        y_ui += 40
        
        # Helper para dibujar métricas con barra
        def draw_metric(label, value, target, is_min, unit="", y_pos=0):
            # Color: Verde si cumple, Rojo si no
            success = (value >= target) if is_min else (value <= target)
            color = (0, 255, 0) if success else (0, 0, 255)
            
            # Etiqueta
            cv2.putText(canvas, label, (x_ui, y_pos), FONT, 0.5, (200, 200, 200), 1)
            
            # Valor
            val_str = f"{value:.2f}{unit}" if isinstance(value, float) else str(value)
            cv2.putText(canvas, val_str, (x_ui + 180, y_pos), FONT, 0.6, color, 2)
            
            # Barra de progreso (visual)
            bar_w = 200
            bar_h = 6
            bar_x = x_ui
            bar_y = y_pos + 8
            
            # Fondo barra
            cv2.rectangle(canvas, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (80, 80, 80), -1)
            
            # Llenado barra
            # Normalizar valor para la barra (0 a 100% o 0 a 1s)
            if unit == "%":
                fill_pct = min(value / 100.0, 1.0)
            elif unit == "s":
                fill_pct = min(value / 1.0, 1.0) # Escala 1s max
            else:
                fill_pct = 0
                
            fill_w = int(bar_w * fill_pct)
            cv2.rectangle(canvas, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), color, -1)
            
            # Marca de objetivo
            if unit == "%":
                target_x = int(bar_w * (target / 100.0))
            elif unit == "s":
                target_x = int(bar_w * target) # Si target es 0.5s, marca a la mitad
            else:
                target_x = 0
                
            cv2.line(canvas, (bar_x + target_x, bar_y - 2), (bar_x + target_x, bar_y + bar_h + 2), (255, 255, 0), 2)

        # 1. Tasa Detección (D)
        draw_metric("Tasa Deteccion (D)", d_rate*100, THRESH_D_MIN*100, True, "%", y_ui)
        y_ui += 50
        
        # 2. Falsos Positivos (FP)
        draw_metric("Falsos Pos. (FP)", fp_rate*100, THRESH_FP_MAX*100, False, "%", y_ui)
        y_ui += 50
        
        # 3. Tiempo Detección (t_det)
        draw_metric("Tiempo Det. (t)", avg_t_det, THRESH_T_DET, False, "s", y_ui)
        y_ui += 50
        
        # 4. Tasa Identificación (S)
        draw_metric("Tasa Identif. (S)", s_id*100, THRESH_S_ID*100, True, "%", y_ui)
        y_ui += 50
        
        # 5. Tiempo Identif. (t_id)
        draw_metric("Tiempo Id. (t)", avg_t_id, THRESH_T_ID, False, "s", y_ui)
        y_ui += 60
        
        # Separador
        cv2.line(canvas, (w, y_ui), (w + panel_w, y_ui), (100, 100, 100), 1)
        y_ui += 30
        
        # Estado Actual
        cv2.putText(canvas, "ESTADO ACTUAL:", (x_ui, y_ui), FONT, 0.5, (200, 200, 200), 1)
        y_ui += 30
        
        status_color = (0, 255, 0) if identified else (0, 255, 255) if detected else (100, 100, 100)
        status_text = "IDENTIFICADO" if identified else "DETECTADO" if detected else "BUSCANDO..."
        
        # Caja de estado
        cv2.rectangle(canvas, (x_ui, y_ui), (x_ui + 240, y_ui + 40), status_color, -1)
        cv2.putText(canvas, status_text, (x_ui + 10, y_ui + 28), FONT, 0.7, (0, 0, 0), 2)
        y_ui += 60
        
        if identified:
            # Mostrar nombre producto grande
            lines = product_name.split(" ")
            for i, line in enumerate(lines):
                cv2.putText(canvas, line, (x_ui, y_ui + (i*25)), FONT, 0.6, (255, 255, 255), 1)

        cv2.imshow(WINDOW_NAME, canvas)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            tracker = PerformanceTracker()
            print("Estadísticas reiniciadas.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

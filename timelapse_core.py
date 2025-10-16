# timelapse_core.py
import cv2
import os
import time
import threading

def detectar_camaras(max_test=10):
    camaras = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camaras.append(i)
            cap.release()
    return camaras

def capture_timelapse(duration_sec, interval_sec, output_fps, output_path="timelapse.mp4", frames_dir="frames", camara=0):
    os.makedirs(frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(camara)
    if not cap.isOpened():
        raise RuntimeError("No se puede acceder a la cámara seleccionada.")

    frame_count = 0
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= duration_sec:
            break

        ret, frame = cap.read()
        if not ret:
            print("Error al capturar frame")
            continue

        filename = os.path.join(frames_dir, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(filename, frame)
        frame_count += 1
        time.sleep(interval_sec)

    cap.release()
    os.system(f"ffmpeg -y -framerate {output_fps} -pattern_type glob -i '{frames_dir}/*.jpg' "
              f"-c:v libx264 -pix_fmt yuv420p '{output_path}'")
    print(f"Timelapse generado en: {output_path}")

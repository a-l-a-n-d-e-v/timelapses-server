# web_server.py
from flask import Flask, render_template, request, jsonify
import threading
import timelapse_core as tl
import os
from datetime import datetime as date
app = Flask(__name__)
timelapse_thread = None

@app.route('/')
def index():
    camaras = tl.detectar_camaras()
    return render_template('index.html', camaras=camaras)

@app.route('/start', methods=['POST'])
def start_timelapse():
    data = request.form
    try:
        camara = int(data.get("camara"))
        duracion = float(data.get("duracion"))
        intervalo = float(data.get("intervalo"))
        fps = int(data.get("fps"))
        path = data.get("path") or "frames_" + date.now().strftime("%Y-%m-%d_%H-%M-%S")

        salida = data.get("salida") or "timelapse.mp4"
        # Validar que la salida sea un archivo .mov, .mp4 o .avi
        if salida.split(".")[-1] not in ["mov", "mp4", "avi"]:
            salida += ".mp4"

        prefix_path = 'resources'
        frames_dir = os.path.join(prefix_path, path, "frames")
        def run_timelapse():
            tl.capture_timelapse(duracion, intervalo, fps, output_path=os.path.join(prefix_path, path, salida), frames_dir=frames_dir, camara=camara)

        global timelapse_thread
        timelapse_thread = threading.Thread(target=run_timelapse, daemon=True)
        timelapse_thread.start()

        return jsonify({"status": "ok", "msg": "Timelapse iniciado correctamente."})

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

@app.route('/status')
def status():
    running = timelapse_thread.is_alive() if timelapse_thread else False
    return jsonify({"running": running})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

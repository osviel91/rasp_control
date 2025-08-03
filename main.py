from flask import Flask, jsonify, request, abort

import subprocess
import os

app = Flask(__name__)

API_KEY = os.environ.get("RASP_CONTROL_API_KEY")
CURRENT_URL = None

ALLOWED_PROGRAMS = {
    'blueman': ['blueman-manager'],
    # 'otro_programa': ['comando']
}

def check_api_key():
    """
    Si se define API_KEY, las peticiones deben incluir el encabezado
    X-API-KEY con el valor correcto. De lo contrario se devuelve 401.
    """
    if API_KEY:
        key = request.headers.get('X-API-KEY')
        if key != API_KEY:
            abort(401)
            
@app.route('/')
def status():
    return jsonify({"status": "OK"})

@app.route('/reboot', methods=['POST'])
def reboot():
    subprocess.Popen(["/sbin/reboot"])
    return jsonify({"action": "rebooting"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    subprocess.Popen(["/sbin/shutdown", "now"])
    return jsonify({"action": "shutting down"})

@app.route('/program/<name>', methods=['POST'])
def start_program(name):
    check_api_key()
    cmd = ALLOWED_PROGRAMS.get(name)
    if not cmd:
        abort(404)
    # Construye la cadena de comando y usa bash para ejecutarla con DISPLAY=:0
    command_str = ' '.join(cmd)
    try:
        subprocess.Popen(
            ['bash', '-c', f'DISPLAY=:0 {command_str}']
        )
        return jsonify({"action": f"starting {name}"})
    except FileNotFoundError:
        return jsonify({"error": f"Program '{name}' not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
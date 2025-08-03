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
    cmd = ALLOWED_PROGRAMS.get(name)
    if not cmd:
        abort(404)
    # Establece DISPLAY para que la aplicación gráfica se abra en la pantalla
    env = dict(os.environ)
    env['DISPLAY'] = env.get('DISPLAY', ':0')
    subprocess.Popen(cmd, env=env)
    return jsonify({"action": f"starting {name}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

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

@app.route('/screen/off', methods=['POST'])
def screen_off():
    subprocess.run(["vcgencmd", "display_power", "0"])
    return jsonify({"action": "screen off"})

@app.route('/screen/on', methods=['POST'])
def screen_on():
    subprocess.run(["vcgencmd", "display_power", "1"])
    return jsonify({"action": "screen on"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
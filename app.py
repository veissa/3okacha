from flask import Flask, request, jsonify
from math import *

app = Flask(__name__)

blacklist = [
    "import", ')', '(', "'", '"', ".", "{", '#', "_", '}', '%', "@", "!", ">", "<", "$", "\\", "~", "?", ";", ":",
    "system", "exec", "execl", "python", "eval", "include", "input", "os.system", "subprocess",
    "pickle", "open", "shutil", "os.", "getattr", "setattr", "delattr", "globals", "locals",
    "compile", "super", "ctypes", "socket", "http", "xml", "json", "yaml", "ast", "re.",
    "hashlib", "random", "tempfile", "sys.", "logging", "sqlite3", "pymysql", "pymongo",
    "ftplib", "smtplib", "ssl", "paramiko", "binascii", "inspect", "tarfile", "zipfile",
    "glob", "multiprocessing", "threading", "concurrent", "time.sleep", "signal", "escape",
    "bizuuuuuuuuuu"
]

quote = """
hacker.target = target
while True:
    hacker.see()
    hacker.learn()
    hacker.see_with_passion()
    hacker.learn()
    hacker_see()
    detect = hacker.detect()
    if detect:
        hacker.exploit()
        break

this is not a part of the challenge it's a life style
"""

@app.route("/", methods=["GET"])
def index():
    # Serve the frontend HTML
    return app.send_static_file("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json(force=True)
    command = data.get("code", "")
    for b in blacklist:
        if b in command:
            return jsonify({
                "error": "are you bizzuuu?",
                "quote": quote
            })
    try:
        # Empty builtins to limit dangerous access
        exec_globals = {}
        exec(command, {"__builtins__": {}}, exec_globals)
        result = eval(command, {"__builtins__": {}}, exec_globals)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "dik chi herban", "details": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)


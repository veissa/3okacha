from flask import Flask, request, jsonify
from math import *

app = Flask(__name__)

blacklist = [
    "import",')','(',"'",'"',".","{",'#',"_",'}','%',"@","!",">","<","$","\\","~","?",";",":","system","exec","execl","python",
    "hhhhhhhhhhhhhhh","lmocha3wid","cit{mniytk}","molat-lkrmoss","eval","include","input","os.system","subprocess",
    "pickle","CIT-wa3rin","open","shutil","os.","getattr","setattr","delattr","globals","locals","compile","super","ctypes",
    "socket","http","xml","json","yaml","ast","re.","hashlib","random","tempfile","sys.","logging","sqlite3","pymysql",
    "pymongo","ftplib","smtplib","ssl","paramiko","binascii","inspect","tarfile","zipfile","glob","multiprocessing",
    "threading","concurrent","time.sleep","signal","escape","bizuuuuuuuuuu"
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
    return "Welcome to the 3okacha Secure Python Jail!"

@app.route("/run", methods=["POST"])
def run_code():
    command = request.json.get("code", "")
    for b in blacklist:
        if b in command:
            return jsonify({
                "error": "are you bizzuuu?",
                "quote": quote
            })

    try:
        exec_globals = {}
        exec(command, {"__builtins__": {}}, exec_globals)
        result = eval(command, {"__builtins__": {}}, exec_globals)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "dik chi herban", "details": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


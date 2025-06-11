from flask import Flask, render_template, request, jsonify
from math import *
import os
import sys
from io import StringIO
import ast
import uuid
import subprocess

app = Flask(__name__)

# Store user contexts
user_contexts = {}

# Make Blacklisted a global variable that can be modified
global_blacklist = ["import",')','(',"'",'"',".","{",'#','_','}','%',"@","!",">","<","$","\\","~","?",";",":","system","exec","execl","python","hhhhhhhhhhhhhhh","charikat dajaj","flag{bniytk}","hayfa2 wahbi","eval","include",
    "eval",
    "exec",
    "input",
    "os.system",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.run",
    "pickle.load",
    "marshal.load",
    "open",
    "shutil.rmtree",
    "shutil.move",
    "shutil.copyfile",
    "shutil.copytree",
    "os.remove",
    "os.rmdir",
    "os.chdir",
    "os.chmod",
    "os.chown",
    "os.link",
    "os.symlink",
    "os.rename",
    "os.walk",
    "os.popen",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "compile",
    "super",
    "ctypes.CDLL",
    "ctypes.windll",
    "ctypes.PyDLL",
    "ctypes.pointer",
    "socket",
    "http.client.HTTPConnection",
    "http.client.HTTPSConnection",
    "xml.etree.ElementTree.parse",
    "xml.etree.ElementTree.fromstring",
    "xml.sax.make_parser",
    "xmlrpc.client.ServerProxy",
    "xmlrpc.server.SimpleXMLRPCServer",
    "xml.dom.minidom.parse",
    "xml.dom.minidom.parseString",
    "json.load",
    "json.loads",
    "yaml.load",
    "ast.literal_eval",
    "ast.parse",
    "ast.dump",
    "ast.NodeVisitor.visit",
    "re.compile",
    "re.sub",
    "hashlib.md5",
    "hashlib.sha1",
    "hashlib.new",
    "random.seed",
    "random.random",
    "random.randint",
    "random.choice",
    "tempfile.mktemp",
    "tempfile.mkdtemp",
    "sys.setrecursionlimit",
    "sys.exit",
    "sys._getframe",
    "sys.modules",
    "logging.basicConfig",
    "sqlite3.connect",
    "pymysql.connect",
    "pymongo.MongoClient",
    "ftplib.FTP",
    "smtplib.SMTP",
    "ssl.wrap_socket",
    "paramiko.SSHClient",
    "binascii.a2b_base64",
    "binascii.b2a_base64",
    "inspect.getmembers",
    "inspect.getmodule",
    "inspect.getsource",
    "tarfile.open",
    "zipfile.ZipFile",
    "glob.glob",
    "multiprocessing.Process",
    "multiprocessing.Pool",
    "threading.Thread",
    "concurrent.futures.ProcessPoolExecutor",
    "concurrent.futures.ThreadPoolExecutor",
    "time.sleep",
    "signal.alarm",
    "signal.pause",
    "flag{mnytak hh}",
    "bizuuuuuuuuuuuuuuuu",
    "lmocha3wid", "rm"
]

HACKER_MESSAGE = """
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

this is not a part of the challenge it's an life style
"""

def is_blacklisted(code, namespace):
    # Always check for "rm" or "app.py" regardless of dynamic blacklist
    if "rm" in code or "app.py" in code:
        return True

    try:
        # Get the current blacklist from the namespace
        current_blacklist = namespace.get('Blacklisted', global_blacklist)
        
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Get all string literals in the code
        string_literals = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Str):
                string_literals.append(node.s)
        
        # Remove string literals from the code for checking
        code_without_strings = code
        for literal in string_literals:
            code_without_strings = code_without_strings.replace(literal, '')
        
        # Check if any blacklisted word is in the code (excluding string literals)
        for b in current_blacklist:
            if b in code_without_strings:
                return True
        return False
    except:
        # If parsing fails, fall back to simple checking
        current_blacklist = namespace.get('Blacklisted', global_blacklist)
        for b in current_blacklist:
            if b in code:
                return True
        return False

def execute_system_command(command):
    try:
        # Use subprocess to capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    command = request.json.get('code', '')
    user_id = request.json.get('user_id', str(uuid.uuid4()))
    
    try:
        # Get or create namespace for this user
        if user_id not in user_contexts:
            user_contexts[user_id] = {}
        
        # Get the user's namespace
        namespace = user_contexts[user_id]
        
        # Capture stdout
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        # Split the command into lines
        lines = command.strip().split('\n')
        all_output = []
        
        # Execute each line separately
        for line in lines:
            if not line.strip():
                continue
                
            # Check blacklist before executing each line
            if is_blacklisted(line, namespace):
                return jsonify({
                    'output': HACKER_MESSAGE + "\nAAAA dak bizuuu, wa fkr chweya ?",
                    'error': True,
                    'user_id': user_id
                })
            
            try:
                # Execute the line
                exec(line, namespace)
                
                # Get the output
                output = redirected_output.getvalue()
                redirected_output.truncate(0)
                redirected_output.seek(0)
                
                # If there's no output from print statements, try to evaluate the expression
                if not output:
                    try:
                        result = eval(line, namespace)
                        if result is not None:
                            output = str(result)
                    except:
                        pass
                
                # If the line contains a system command, execute it and get its output
                if 'os.system' in line:
                    # Extract the command from os.system('command')
                    cmd = line.split('os.system(')[1].split(')')[0].strip("'\"")
                    output = execute_system_command(cmd)
                
                if output:
                    all_output.append(output)
                
            except Exception as e:
                all_output.append(f"dak chi herban: {str(e)}")
        
        # Restore stdout
        sys.stdout = old_stdout
        
        # Update the user's namespace
        user_contexts[user_id] = namespace
        
        # Return all output
        return jsonify({
            'output': '\n'.join(all_output),
            'error': False,
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({
            'output': f"dak chi herban: {str(e)}",
            'error': True,
            'user_id': user_id
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

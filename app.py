from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timezone
import ast
import operator
import os
import platform

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Deliberately limited arithmetic evaluator. This is NOT a general Python sandbox.
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARYOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def safe_math(expression: str):
    if len(expression) > 160:
        raise ValueError("Expression is too long.")
    tree = ast.parse(expression, mode="eval")

    def visit(node, depth=0):
        if depth > 20:
            raise ValueError("Expression is too complex.")
        if isinstance(node, ast.Expression):
            return visit(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 10**12:
                raise ValueError("Number is too large.")
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large.")
            result = _ALLOWED_BINOPS[type(node.op)](left, right)
            if isinstance(result, (int, float)) and abs(result) > 10**15:
                raise ValueError("Result is too large.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[type(node.op)](visit(node.operand, depth + 1))
        raise ValueError("Only basic arithmetic is supported here.")

    return visit(tree)

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "app": "MADDY OS API",
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "host": platform.system()
    })

@app.post("/api/terminal")
def terminal():
    body = request.get_json(silent=True) or {}
    command = str(body.get("command", "")).strip()
    if not command:
        return jsonify({"output": ""})

    # Safe demo commands only. Never pass user input to a shell or exec().
    if command == "help":
        output = "Available demo commands: help, clear, date, uname, whoami, pwd, ls"
    elif command == "date":
        output = datetime.now().astimezone().isoformat(timespec="seconds")
    elif command == "uname":
        output = "MADDY-OS web desktop (API host: " + platform.system() + ")"
    elif command == "whoami":
        output = "guest"
    elif command == "pwd":
        output = "/home/guest"
    elif command == "ls":
        output = "Desktop  Documents  Downloads  Pictures"
    elif command == "clear":
        output = "__CLEAR__"
    else:
        output = (
            "Command not available in the safe demo terminal: " + command +
            "\nThis web terminal does not execute arbitrary shell commands."
        )
    return jsonify({"output": output})

@app.post("/api/python-math")
def python_math():
    body = request.get_json(silent=True) or {}
    expression = str(body.get("expression", ""))
    try:
        result = safe_math(expression)
        return jsonify({"ok": True, "result": result})
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)

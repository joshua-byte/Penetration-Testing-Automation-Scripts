
from flask import Flask, jsonify

app = Flask(__name__)

# Intentionally exposed test routes
@app.route("/")
def home():
    return "Local VAPT Test Server"

@app.route("/admin")
def admin():
    return "Test admin page - no real credentials"

@app.route("/backup")
def backup():
    return "Test backup file"

@app.route("/uploads")
def uploads():
    return "Test uploads directory"

@app.route("/forbidden")
def forbidden():
    return "Access forbidden", 403

@app.route("/old-panel")
def old_panel():
    return "Redirecting...", 302

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

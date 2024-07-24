from flask import Flask, send_from_directory
import json

app = Flask(__name__)

@app.route("/")
def serve_json():
    return send_from_directory('templates', 'dump3.json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

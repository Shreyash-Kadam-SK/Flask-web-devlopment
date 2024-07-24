from flask import Flask, request, jsonify,send_from_directory
import json
import os

app = Flask(__name__)

@app.route("/update", methods=["PUT"])
def update_json():
    # Path to the JSON file
    json_file_path = 'templates/dump3.json'

    # Check if the file exists
    if not os.path.exists(json_file_path):
        return jsonify({"error": "File not found"}), 404

    # Read the existing data
    with open(json_file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400

    # Get the new data from the request
    new_data = request.json

    # Update the data
    data.update(new_data)

    # Write the updated data back to the file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify(data), 200


@app.route("/show")
def serve_json():
    return send_from_directory('templates', 'dump3.json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

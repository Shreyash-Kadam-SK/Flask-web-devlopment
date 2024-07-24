from flask import Flask, request, jsonify, send_from_directory
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

    # Check if the existing data is a list
    if isinstance(data, dict) and "Employers" in data:
        if isinstance(new_data, dict) and "Employers" in new_data:
            data["Employers"].extend(new_data["Employers"])
        else:
            return jsonify({"error": "New data must be a dictionary with 'Employers' key"}), 400
    else:
        return jsonify({"error": "Unsupported JSON format"}), 400

    # Write the updated data back to the file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify(data), 200

@app.route("/delete/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
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

    # Check if the existing data is a list
    if isinstance(data, dict) and "Employers" in data:
        # Find and remove the employee with the given emp_id
        data["Employers"] = [emp for emp in data["Employers"] if emp["emp_id"] != emp_id]
    else:
        return jsonify({"error": "Unsupported JSON format"}), 400

    # Write the updated data back to the file
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


    return jsonify(data), 200

@app.route("/show")
def serve_json():
    return send_from_directory('templates', 'dump3.json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

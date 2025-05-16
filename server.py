from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        data = request.json
        if not data or 'value1' not in data or 'value2' not in data:
            return jsonify({"error": "No data provided or 'value1' or 'value2' not found"}), 400

        value1 = data['value1']
        value2 = data['value2']

        # Попытка преобразовать строки в числа, если это возможно
        if isinstance(value1, str):
            try:
                value1 = float(value1)
            except ValueError:
                return jsonify({"error": "value1 must be a number"}), 400
        
        if isinstance(value2, str):
            try:
                value2 = float(value2)
            except ValueError:
                return jsonify({"error": "value2 must be a number"}), 400

        if not isinstance(value1, (int, float)) or not isinstance(value2, (int, float)):
            return jsonify({"error": "Both values must be numbers"}), 400

        rounded_value1 = round(value1, 1)
        rounded_value2 = round(value2, 1)

        return jsonify({
            "rounded_value1": rounded_value1,
            "rounded_value2": rounded_value2
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

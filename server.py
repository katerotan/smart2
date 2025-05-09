from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        data = request.json
        if not data or 'value' not in data:
            return jsonify({"error": "No data provided or 'value' not found"}), 400

        value = data['value']

        # Попытка преобразовать строку в число, если это возможно
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return jsonify({"error": "Value must be a number"}), 400

        if not isinstance(value, (int, float)):
            return jsonify({"error": "Value must be a number"}), 400

        rounded_value = round(value, 2)

        return jsonify({"rounded_value": rounded_value}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        data = request.json
        if not data or 'weight_kg' not in data:
            return jsonify({"error": "No data provided or 'weight_kg' not found"}), 400

        weight_kg = data['weight_kg']

        # Перевірка типу даних
        if isinstance(weight_kg, str):
            try:
                weight_kg = float(weight_kg)
            except ValueError:
                return jsonify({"error": "Weight must be a number"}), 400

        if not isinstance(weight_kg, (int, float)):
            return jsonify({"error": "Weight must be a number"}), 400

        # Формули розрахунку дозування з округленням до десятих
        augmentin_es_dose = round(((90 * weight_kg) / 2) / 120, 1)
        augmentin_400_70_dose = round(((70 * weight_kg) / 2) / 80, 1)
        augmentin_400_45_dose = round(((45 * weight_kg) / 2) / 80, 1)
        augmentin_200_70_dose = round(((70 * weight_kg) / 2) / 40, 1)
        augmentin_200_45_dose = round(((45 * weight_kg) / 2) / 40, 1)

        # Формування повідомлень для кожного типу препарату
        if weight_kg <= 45:
            message_es = (
                f"<b>Аугментин ES</b><br>"
                f"600 мг / 5 мл + 42,9 / 5 мл<br>"
                f"фл. 100 мл. № 1<br>"
                f"🔸🔸🔸<br>"
                f"👧👦Для дітей вагою <b>{weight_kg}</b> кг<br>"
                f"cлід призначити по <b>{augmentin_es_dose}</b> мл<br>"
                f"🥛 2 рази на добу<br>"
                f"🔸🔸🔸<br>"
                f"Для більш детальної інформації розгляньте інструкцію🔎📘"
            )
            message_400 = (
                f"<b>Аугментин 400 мг</b><br>"
                f"400 мг / 5 мл + 57 мг / 5 мл<br>"
                f"фл. для приготування 70 мл сусп. № 1<br>"
                f"🔸🔸🔸<br>"
                f"👧👦Для дітей вагою <b>{weight_kg}</b> кг<br>"
                f"При дозуванні 45 мг/кг: <b>{augmentin_400_45_dose}</b> мл<br>"
                f"При дозуванні 70 мг/кг: <b>{augmentin_400_70_dose}</b> мл<br>"
                f"🥛 2 рази на добу<br>"
                f"🔸🔸🔸<br>"
                f"Для більш детальної інформації розгляньте інструкцію🔎📘"
            )
            message_200 = (
                f"<b>Аугментин 200 мг</b><br>"
                f"200 мг / 5 мл + 28,5 мг / 5 мл<br>"
                f"фл. для приготування 70 мл сусп. № 1<br>"
                f"🔸🔸🔸<br>"
                f"👧👦Для дітей вагою <b>{weight_kg}</b> кг<br>"
                f"При дозуванні 45 мг/кг: <b>{augmentin_200_45_dose}</b> мл<br>"
                f"При дозуванні 70 мг/кг: <b>{augmentin_200_70_dose}</b> мл<br>"
                f"🥛 2 рази на добу<br>"
                f"🔸🔸🔸<br>"
                f"Для більш детальної інформації розгляньте інструкцію🔎📘"
            )
        else:
            message_es = "Для ваги більше 45 кг існує інший розрахунок для Аугментину ES. Більш детальна інформація в інструкції."
            message_400 = "Для ваги більше 45 кг існує інший розрахунок для Аугментину 400 мг. Більш детальна інформація в інструкції."
            message_200 = "Для ваги більше 45 кг існує інший розрахунок для Аугментину 200 мг. Більш детальна інформація в інструкції."

        # Відправка відповіді з розрахованими дозами та повідомленнями
        response = {
            "augmentin_es_dose": augmentin_es_dose,
            "augmentin_400_70_dose": augmentin_400_70_dose,
            "augmentin_400_45_dose": augmentin_400_45_dose,
            "augmentin_200_70_dose": augmentin_200_70_dose,
            "augmentin_200_45_dose": augmentin_200_45_dose,
            "message_es": message_es,
            "message_400": message_400,
            "message_200": message_200
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
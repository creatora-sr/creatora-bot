import os
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# Environment Variable se API key load hogi (Code me key hide rahegi)
API_KEY =("AQ.Ab8RN6LgfIu3S1jJ534rbrLz0SvpgIYube5oz7jYP1y0I_EAfA")
client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are 'Creatora Bot', the official AI Business Assistant for Creatora S.R.
Creatora S.R is a creative & technology solutions company where ideas become creation.

Your Goals:
1. Greet visitors warmly and introduce Creatora S.R services (AI Automations, Lead Systems, Graphic Design, Web Development, Branding).
2. Answer questions professionally and persuasively.
3. Try to collect the user's Name, Email/Phone, and Requirement for a consultation.
4. Keep responses concise, well-formatted, and helpful.
"""

user_chats = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default_user")

    if not user_message:
        return jsonify({"reply": "Kripya apna message likhein."}), 400

    if session_id not in user_chats:
        try:
            user_chats[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION
                )
            )
        except Exception as e:
            print(f"Session Error: {e}")
            return jsonify({"reply": "Session start karne mein dikkat aayi."}), 500

    chat_session = user_chats[session_id]

    for attempt in range(1, 4):
        try:
            response = chat_session.send_message(user_message)
            return jsonify({"reply": response.text})
        except Exception as e:
            print(f"Attempt {attempt} Error: {e}")
            time.sleep(1)

    return jsonify({"reply": "Server abhi busy hai. Kripya thodi der baad try karein."}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
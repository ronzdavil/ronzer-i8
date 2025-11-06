from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder="../templates")

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": "Bearer YOUR_HF_API_KEY"}  # Replace with your Hugging Face key

SYSTEM_PROMPT = (
    "You are Ronzer I8, an advanced AI assistant created by RonzDavil. "
    "Always respond clearly, naturally, and intelligently. "
    "When asked about your creator or identity, say 'I am Ronzer I8, created by RonzDavil.'"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    prompt = f"{SYSTEM_PROMPT}\nUser: {user_message}\nRonzer:"
    response = requests.post(HF_API_URL, headers=HEADERS, json={"inputs": prompt})
    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        reply = result[0]["generated_text"].split("Ronzer:")[-1].strip()
    else:
        reply = "Sorry, I couldn’t process that right now."

    return jsonify({"reply": reply})

def handler(request, *args, **kwargs):
    return app(request.environ, lambda status, headers: (status, headers, []))

from flask import Flask, render_template, request, jsonify
import ollama
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
HISTORY_FILE = "chat_history.json"

# Load chat history if exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        chat_history = json.load(file)
else:
    chat_history = []

from flask import Flask, render_template, request, jsonify, redirect, url_for, session

@app.route("/")
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "No message received"}), 400

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Generate response using DeepSeek-R1
    response = ollama.chat(model="deepseek-r1:8b", messages=chat_history)

    bot_reply = response['message']['content']
    
    # Append bot response to chat history
    chat_history.append({"role": "assistant", "content": bot_reply})

    # Save updated chat history
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4)

    return jsonify({"bot": bot_reply})

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

SECRET_NUMBER = "1234"  # Replace with a more secure method in a real application

@app.route('/manual_login', methods=['POST'])
def manual_login():
    try:
        data = request.get_json()
        number = data.get('number')

        if number == SECRET_NUMBER:
            session['logged_in'] = True
            return jsonify({"status": "success", "message": "Login successful!"})
        else:
            return jsonify({"status": "failure", "message": "Incorrect number. Try again."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
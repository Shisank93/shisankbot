import ollama
import json
import os

# File to store chat history
HISTORY_FILE = "chat_history.json"

# Load chat history if exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        chat_history = json.load(file)
else:
    chat_history = []

print("DeepSeek-R1 Chatbot is ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot session ended.")
        break

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Generate response using DeepSeek-R1
    response = ollama.chat(model="deepseek-r1:8b", messages=chat_history)

    bot_reply = response['message']['content']
    print("Bot:", bot_reply)

    # Append bot response to chat history
    chat_history.append({"role": "assistant", "content": bot_reply})

    # Save updated chat history
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4)
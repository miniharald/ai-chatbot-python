from app.chatbot import load_system_prompt, ask_chatbot

def chat():
    messages = [
        {"role": "system", "content": load_system_prompt()}
    ]

    print("Please type in your question below. Write 'exit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})
        reply = ask_chatbot(messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"\nAI: {reply}\n")

if __name__ == "__main__":
    chat()

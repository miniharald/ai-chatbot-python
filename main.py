from app.chatbot import (
    load_system_prompt, 
    ask_chatbot, 
    get_available_models, 
    set_model, 
    get_current_model,
    estimate_cost
)

def display_available_models():
    models = get_available_models()
    current = get_current_model()
    
    print("\n📋 Available Models:")
    print("-" * 60)
    for model_id, info in models.items():
        status = "✅ Current" if model_id == current['id'] else "  "
        print(f"{status} {model_id}")
        print(f"    📖 {info['description']}")
        print(f"    💰 Cost: ${info['cost_per_1k_tokens']['input']}/1K input, ${info['cost_per_1k_tokens']['output']}/1K output tokens")
        print()

def change_model():
    display_available_models()
    
    while True:
        choice = input("Enter model name (or 'cancel' to abort): ").strip()
        if choice.lower() == 'cancel':
            return
        
        if set_model(choice):
            current = get_current_model()
            print(f"✅ Model changed to: {current['info']['name']}")
            break
        else:
            print(f"❌ Invalid model: {choice}")

def show_current_model():
    current = get_current_model()
    print(f"\n🤖 Current Model: {current['info']['name']} ({current['id']})")
    print(f"📖 {current['info']['description']}")

def display_help():
    print("\n🔧 Available Commands:")
    print("  /models  - View available models")
    print("  /switch  - Change current model")
    print("  /current - Show current model")
    print("  /cost    - Show estimated cost for next message")
    print("  /help    - Show this help")
    print("  exit     - Exit the program")
    print()

def handle_command(command: str, messages: list) -> bool:
    command = command.lower().strip()
    
    if command == "/models":
        display_available_models()
        return True
    elif command == "/switch":
        change_model()
        return True
    elif command == "/current":
        show_current_model()
        return True
    elif command == "/cost":
        cost = estimate_cost(messages)
        print(f"\n💰 Estimated cost for next message: ${cost['total']:.6f}")
        print(f"   Input: ${cost['input']:.6f}, Output: ${cost['output']:.6f}")
        return True
    elif command == "/help":
        display_help()
        return True
    
    return False

def chat():
    messages = [
        {"role": "system", "content": load_system_prompt()}
    ]

    print("🤖 AI Chatbot with Multi-Model Support")
    show_current_model()
    print("\nType your question below, or use commands starting with '/' (type '/help' for commands)")
    print("Type 'exit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            break
        
        if user_input.startswith('/'):
            if handle_command(user_input, messages):
                continue
            else:
                print("❌ Unknown command. Type '/help' for available commands.")
                continue
        
        if not user_input:
            continue
        
        cost = estimate_cost(messages + [{"role": "user", "content": user_input}])
        print(f"💰 Estimated cost: ${cost['total']:.6f}")
        
        messages.append({"role": "user", "content": user_input})
        reply = ask_chatbot(messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"\nAI: {reply}\n")

if __name__ == "__main__":
    chat()

from app.chatbot import (
    load_system_prompt, 
    ask_chatbot, 
    get_available_models, 
    set_model, 
    get_current_model,
    estimate_cost,
    get_available_prompts,
    set_prompt,
    get_current_prompt,
    create_custom_prompt
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

def display_available_prompts():
    prompts = get_available_prompts()
    current = get_current_prompt()
    
    print("\n📝 Available Prompts:")
    print("-" * 60)
    
    # Group by category
    categories = {}
    for prompt_id, info in prompts.items():
        category = info.get('category', 'general')
        if category not in categories:
            categories[category] = []
        categories[category].append((prompt_id, info))
    
    for category, prompt_list in categories.items():
        print(f"\n📂 {category.title()}:")
        for prompt_id, info in prompt_list:
            status = "✅ Current" if prompt_id == current['id'] else "  "
            print(f"{status} {prompt_id}")
            print(f"    📋 {info['name']}")
            print(f"    💭 {info['description']}")
        print()

def change_prompt():
    display_available_prompts()
    
    while True:
        choice = input("Enter prompt ID (or 'cancel' to abort): ").strip()
        if choice.lower() == 'cancel':
            return
        
        if set_prompt(choice):
            current = get_current_prompt()
            print(f"✅ Prompt changed to: {current['info']['name']}")
            break
        else:
            print(f"❌ Invalid prompt: {choice}")

def show_current_prompt():
    current = get_current_prompt()
    print(f"\n📝 Current Prompt: {current['info']['name']} ({current['id']})")
    print(f"💭 {current['info']['description']}")

def create_new_custom_prompt():
    print("\n🎨 Create Custom Prompt")
    print("-" * 40)
    
    prompt_id = input("Enter prompt ID (no spaces, use underscores): ").strip().lower().replace(' ', '_')
    if not prompt_id:
        print("❌ Prompt ID cannot be empty")
        return
    
    existing_prompts = get_available_prompts()
    if prompt_id in existing_prompts:
        print(f"❌ Prompt ID '{prompt_id}' already exists")
        return
    
    name = input("Enter prompt name: ").strip()
    if not name:
        print("❌ Prompt name cannot be empty")
        return
    
    description = input("Enter prompt description: ").strip()
    if not description:
        print("❌ Prompt description cannot be empty")
        return
    
    category = input("Enter category (or press Enter for 'custom'): ").strip() or "custom"
    
    print(f"\nEnter the prompt content (press Ctrl+D on Unix/Linux/Mac or Ctrl+Z+Enter on Windows when done):")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    
    content = '\n'.join(content_lines).strip()
    
    if not content:
        print("❌ Prompt content cannot be empty")
        return
    
    if create_custom_prompt(prompt_id, name, description, content, category):
        print(f"✅ Custom prompt '{name}' created successfully!")
        
        switch = input("Switch to this prompt now? (y/n): ").strip().lower()
        if switch == 'y' or switch == 'yes':
            set_prompt(prompt_id)
            print(f"✅ Switched to '{name}' prompt")
    else:
        print("❌ Failed to create custom prompt")

def display_help():
    print("\n🔧 Available Commands:")
    print("  /models    - View available models")
    print("  /switch    - Change current model")
    print("  /current   - Show current model")
    print("  /prompts   - View available prompts")
    print("  /persona   - Change current prompt/persona")
    print("  /prompt    - Show current prompt")
    print("  /create    - Create custom prompt")
    print("  /cost      - Show estimated cost for next message")
    print("  /help      - Show this help")
    print("  exit       - Exit the program")
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
    elif command == "/prompts":
        display_available_prompts()
        return True
    elif command == "/persona":
        change_prompt()
        return True
    elif command == "/prompt":
        show_current_prompt()
        return True
    elif command == "/create":
        create_new_custom_prompt()
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

    print("🤖 AI Chatbot with Enhanced Multi-Model & Prompt Support")
    show_current_model()
    show_current_prompt()
    print("\nType your question below, or use commands starting with '/' (type '/help' for commands)")
    print("Type 'exit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            break
        
        if user_input.startswith('/'):
            if handle_command(user_input, messages):
                if user_input.lower() in ['/persona', '/create']:
                    messages[0] = {"role": "system", "content": load_system_prompt()}
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

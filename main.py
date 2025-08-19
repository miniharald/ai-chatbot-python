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
    create_custom_prompt,
    create_conversation,
    save_message_to_db,
    load_conversation,
    list_recent_conversations,
    search_conversation_history,
    delete_conversation_history,
    get_conversation_stats,
    export_conversation,
    cleanup_duplicate_system_messages
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

def show_conversation_history():
    conversations = list_recent_conversations(15)
    
    if not conversations:
        print("\n📚 No conversation history found.")
        return
    
    print("\n📚 Recent Conversations:")
    print("-" * 80)
    
    for conv in conversations:
        title = conv['title'][:50] + "..." if len(conv['title']) > 50 else conv['title']
        created = conv['created_at'][:16]
        cost = f"${conv['total_cost']:.6f}" if conv['total_cost'] else "$0.000000"
        
        print(f"🆔 {conv['id']:3} | 📝 {title:35} | 📅 {created} | 💬 {conv['message_count']:3} msgs | 💰 {cost}")
    print()

def load_conversation_by_id():
    show_conversation_history()
    
    try:
        conv_id = int(input("Enter conversation ID to load (or 0 to cancel): "))
        if conv_id == 0:
            return None
        
        messages = load_conversation(conv_id)
        if messages:
            print(f"✅ Loaded conversation {conv_id}")
            return messages, conv_id
        else:
            print(f"❌ Conversation {conv_id} not found")
            return None
    except ValueError:
        print("❌ Invalid conversation ID")
        return None

def search_conversations():
    query = input("Enter search query: ").strip()
    if not query:
        return
    
    results = search_conversation_history(query, 10)
    
    if not results:
        print(f"🔍 No conversations found matching '{query}'")
        return
    
    print(f"\n🔍 Search Results for '{query}':")
    print("-" * 60)
    
    for conv in results:
        title = conv['title'][:40] + "..." if len(conv['title']) > 40 else conv['title']
        created = conv['created_at'][:16]
        
        print(f"🆔 {conv['id']:3} | 📝 {title:30} | 📅 {created} | 💬 {conv['message_count']:3} msgs")
    print()

def delete_conversation():
    show_conversation_history()
    
    try:
        conv_id = int(input("Enter conversation ID to delete (or 0 to cancel): "))
        if conv_id == 0:
            return
        
        confirm = input(f"Are you sure you want to delete conversation {conv_id}? (y/N): ").strip().lower()
        if confirm == 'y' or confirm == 'yes':
            if delete_conversation_history(conv_id):
                print(f"✅ Conversation {conv_id} deleted")
            else:
                print(f"❌ Failed to delete conversation {conv_id}")
        else:
            print("Delete cancelled")
    except ValueError:
        print("❌ Invalid conversation ID")

def show_usage_stats():
    stats = get_conversation_stats()
    
    print("\n📊 Usage Statistics:")
    print("-" * 40)
    print(f"📚 Total Conversations: {stats['total_conversations']}")
    print(f"💬 Total Messages: {stats['total_messages']}")
    print(f"💰 Total Cost: ${stats['total_cost']:.6f}")
    print(f"🤖 Models Used: {stats['models_used']}")
    print(f"🎭 Prompts Used: {stats['prompts_used']}")
    print()

def export_conversation_menu():
    show_conversation_history()
    
    try:
        conv_id = int(input("Enter conversation ID to export (or 0 to cancel): "))
        if conv_id == 0:
            return
        
        format_choice = input("Export format (json/txt): ").strip().lower()
        if format_choice not in ['json', 'txt']:
            format_choice = 'txt'
        
        try:
            exported_data = export_conversation(conv_id, format_choice)
            filename = f"conversation_{conv_id}.{format_choice}"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exported_data)
            
            print(f"✅ Conversation exported to {filename}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
    except ValueError:
        print("❌ Invalid conversation ID")

def display_help():
    print("\n🔧 Available Commands:")
    print("  /models    - View available models")
    print("  /switch    - Change current model")
    print("  /current   - Show current model")
    print("  /prompts   - View available prompts")
    print("  /persona   - Change current prompt/persona")
    print("  /prompt    - Show current prompt")
    print("  /create    - Create custom prompt")
    print("  /history   - View recent conversations")
    print("  /load      - Load a previous conversation")
    print("  /search    - Search conversation history")
    print("  /delete    - Delete a conversation")
    print("  /export    - Export a conversation")
    print("  /stats     - Show usage statistics")
    print("  /cleanup   - Remove duplicate system messages")
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
    elif command == "/history":
        show_conversation_history()
        return True
    elif command == "/load":
        result = load_conversation_by_id()
        if result:
            new_messages, conv_id = result
            return ('load_conversation', new_messages, conv_id)
        return True
    elif command == "/search":
        search_conversations()
        return True
    elif command == "/delete":
        delete_conversation()
        return True
    elif command == "/export":
        export_conversation_menu()
        return True
    elif command == "/stats":
        show_usage_stats()
        return True
    elif command == "/cleanup":
        deleted = cleanup_duplicate_system_messages()
        if deleted > 0:
            print(f"✅ Cleaned up {deleted} duplicate system messages")
        else:
            print("✅ No duplicate system messages found")
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

    conversation_id = create_conversation()
    print(f"🆔 Started new conversation (ID: {conversation_id})")
    
    save_message_to_db(conversation_id, "system", messages[0]["content"])

    print("🤖 AI Chatbot with Enhanced Multi-Model & Prompt Support + History")
    show_current_model()
    show_current_prompt()
    print("\nType your question below, or use commands starting with '/' (type '/help' for commands)")
    print("Type 'exit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            break
        
        if user_input.startswith('/'):
            result = handle_command(user_input, messages)
            if isinstance(result, tuple) and result[0] == 'load_conversation':
                _, loaded_messages, loaded_conv_id = result
                messages = loaded_messages
                conversation_id = loaded_conv_id
                print(f"🔄 Switched to conversation {conversation_id}")
                continue
            elif result:
                if user_input.lower() in ['/persona', '/create']:
                    new_system_content = load_system_prompt()
                    if messages[0]["content"] != new_system_content:
                        messages[0] = {"role": "system", "content": new_system_content}
                        save_message_to_db(conversation_id, "system", new_system_content)
                        print("🔄 System prompt updated")
                continue
            else:
                print("❌ Unknown command. Type '/help' for available commands.")
                continue
        
        if not user_input:
            continue
        
        cost = estimate_cost(messages + [{"role": "user", "content": user_input}])
        print(f"💰 Estimated cost: ${cost['total']:.6f}")
        
        save_message_to_db(conversation_id, "user", user_input)
        messages.append({"role": "user", "content": user_input})
        print("\nAI: ", end="", flush=True)
        from app.chatbot import ask_chatbot_stream
        reply = ask_chatbot_stream(messages)
        save_message_to_db(conversation_id, "assistant", reply, cost=cost['total'])
        messages.append({"role": "assistant", "content": reply})
        print()

if __name__ == "__main__":
    chat()

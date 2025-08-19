# AI Chatbot with Multi-Model Support & Enhanced Prompt Management

## Features

- **Multiple OpenAI Models**: Support for GPT-4o, GPT-4o Mini, and GPT-3.5 Turbo
- **Model Switching**: Change models during conversation
- **Enhanced Prompt Management**: Multiple AI personas and custom prompts
- **Cost Estimation**: See estimated costs before making requests
- **Configuration Persistence**: Settings are saved between sessions
- **Interactive Commands**: Use commands starting with `/` for special actions
- **Conversation History**: Automatic saving and management of conversation history
- **Streaming Responses**: Real-time response streaming to the terminal
- **Stop Feature**: Interrupt responses anytime with `Ctrl+C`

## Usage

### Basic Chat
```bash
python main.py
```

### Available Commands
- `/models` - View available models and their details
- `/switch` - Change the current model
- `/current` - Show current model information
- `/prompts` - View available prompt templates
- `/persona` - Switch between AI personas
- `/prompt` - Show current prompt information
- `/create` - Create custom prompt templates
- `/cost` - Show estimated cost for next message
- `/help` - Show available commands
- `exit` - Exit the program
- `/history` — View recent conversations
- `/load` — Resume a previous conversation
- `/search` — Search conversation history
- `/export` — Export a conversation to TXT or JSON
- `/delete` — Delete a conversation
- `/stats` — Show usage statistics (total chats, messages, cost, etc.)

### Available Prompt Templates

| Persona | Category | Best For |
|---------|----------|----------|
| Default Assistant | General | General-purpose conversations |
| Coding Assistant | Programming | Code review, debugging, programming help |
| Creative Writer | Creative | Storytelling, creative writing, brainstorming |
| Tutor | Education | Learning, explanations, teaching |
| Business Advisor | Business | Strategy, planning, business advice |
| Research Assistant | Research | Data analysis, research methodology |

### Model Information

| Model | Best For | Cost (per 1K tokens) |
|-------|----------|---------------------|
| GPT-4o | Complex tasks, highest quality | $0.005 input, $0.015 output |
| GPT-4o Mini | Balanced performance and cost | $0.00015 input, $0.0006 output |
| GPT-3.5 Turbo | Fast responses, basic tasks | $0.0005 input, $0.0015 output |

## Configuration

Settings are automatically saved in `config.json`:
- `model`: Current model selection
- `temperature`: Response creativity (0.0-2.0)
- `max_tokens`: Maximum response length

## 🗃️ Conversation History & SQLite Integration

Your chat history is automatically saved to a local SQLite database (`conversations.db`). This enables:

- **Automatic saving** of all conversations and messages
- **Resume any conversation** with `/load`
- **View recent conversations** with `/history`
- **Search your chat history** with `/search`
- **Export conversations** to TXT or JSON with `/export`
- **Delete conversations** with `/delete`
- **View usage statistics** with `/stats`

### Example Usage

```bash
You: /history
# Shows a list of recent conversations
You: /load
# Loads a selected conversation so you can continue
You: /search
# Finds conversations by keyword
You: /export
# Saves a conversation to a file
You: /delete
# Removes a conversation from history
You: /stats
# Shows usage statistics
```

**Note:** Your chat history is stored locally and is private by default. The database file is ignored by git for privacy.

## ⚡ Streaming Responses & Stop Feature

- **Real-time streaming:** AI responses appear in your terminal as they are generated, for a ChatGPT-like experience.
- **Interrupt anytime:** Press `Ctrl+C` during a response to stop streaming and return to the prompt. The bot will continue running and save the partial response.

### Example
```bash
You: Tell me a story about a robot
AI: Once upon a time... (response streams in real time)
# Press Ctrl+C to stop the response early
⏹️ Response stopped by user.
```

## 🎨 Rich Markdown & Code Output

- **Formatting:** AI responses are rendered with Markdown, including bold, italics, lists, and tables.
- **Code highlighting:** Code blocks are automatically detected and displayed with syntax highlighting.
- **Tables and more:** Markdown tables and other elements are shown in the terminal for easy reading.

### Example
```bash
You: Show me a Python function
AI:
```python
def greet(name):
    print(f"Hello, {name}!")
```
# The code block will be highlighted in your terminal!
```

## 📂 File Upload & Analysis

- **Upload files for AI analysis:** Use `/upload` to send a TXT or Python file to the chatbot.
- **Code review:** The bot will review Python files and suggest improvements.
- **Document summary:** The bot will summarize the main points of TXT documents.

### Example
```bash
You: /upload
Enter the path to the file to upload (TXT or .py): myscript.py
AI analysis:
# The bot reviews your code and gives feedback, with Markdown and code highlighting.
```

Supported file types: `.txt`, `.py`

## Best Practices Implemented

1. **Error Handling**: Graceful handling of API errors
2. **Cost Awareness**: Real-time cost estimation
3. **Configuration Management**: Persistent settings
4. **Model Validation**: Ensures selected models are available
5. **Type Hints**: Better code documentation and IDE support
6. **Modular Design**: Separation of concerns between modules

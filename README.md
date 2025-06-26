# AI Chatbot with Multi-Model Support & Enhanced Prompt Management

## Features

- **Multiple OpenAI Models**: Support for GPT-4o, GPT-4o Mini, and GPT-3.5 Turbo
- **Model Switching**: Change models during conversation
- **Enhanced Prompt Management**: Multiple AI personas and custom prompts
- **Cost Estimation**: See estimated costs before making requests
- **Configuration Persistence**: Settings are saved between sessions
- **Interactive Commands**: Use commands starting with `/` for special actions

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

## Best Practices Implemented

1. **Error Handling**: Graceful handling of API errors
2. **Cost Awareness**: Real-time cost estimation
3. **Configuration Management**: Persistent settings
4. **Model Validation**: Ensures selected models are available
5. **Type Hints**: Better code documentation and IDE support
6. **Modular Design**: Separation of concerns between modules

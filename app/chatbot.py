import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AVAILABLE_MODELS = {
    "gpt-4o": {
        "name": "GPT-4o",
        "description": "Most capable model, best for complex tasks",
        "max_tokens": 4096,
        "cost_per_1k_tokens": {"input": 0.005, "output": 0.015}
    },
    "gpt-4o-mini": {
        "name": "GPT-4o Mini", 
        "description": "Faster and more cost-effective version of GPT-4o",
        "max_tokens": 16384,
        "cost_per_1k_tokens": {"input": 0.00015, "output": 0.0006}
    },
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "description": "Fast and efficient for most conversations",
        "max_tokens": 4096,
        "cost_per_1k_tokens": {"input": 0.0005, "output": 0.0015}
    }
}

class PromptManager:
    def __init__(self):
        self.prompts_dir = "app/prompts"
        self.config_file = os.path.join(self.prompts_dir, "prompts_config.json")
        self.prompts = {}
        self.current_prompt = "default"
        self.load_prompts_config()
    
    def load_prompts_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.prompts = config.get('prompts', {})
                    self.current_prompt = config.get('current_prompt', 'default')
            else:

                self.create_default_config()
        except Exception as e:
            print(f"Warning: Could not load prompts config: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        self.prompts = {
            "default": {
                "name": "Default Assistant",
                "description": "General-purpose helpful assistant",
                "file": "default.txt",
                "category": "general"
            }
        }
        self.current_prompt = "default"
        self.save_config()
    
    def save_config(self):
        try:
            config = {
                "prompts": self.prompts,
                "current_prompt": self.current_prompt
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save prompts config: {e}")
    
    def get_available_prompts(self) -> Dict:
        return self.prompts
    
    def get_current_prompt(self) -> Dict:
        if self.current_prompt in self.prompts:
            return {
                'id': self.current_prompt,
                'info': self.prompts[self.current_prompt]
            }
        return {
            'id': 'default',
            'info': {'name': 'Default', 'description': 'Default assistant'}
        }
    
    def set_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self.prompts:
            self.current_prompt = prompt_id
            self.save_config()
            return True
        return False
    
    def load_prompt_content(self, prompt_id: Optional[str] = None) -> str:
        prompt_to_use = prompt_id or self.current_prompt
        
        if prompt_to_use not in self.prompts:
            prompt_to_use = "default"
        
        prompt_info = self.prompts.get(prompt_to_use, {})
        filename = prompt_info.get('file', 'default.txt')
        filepath = os.path.join(self.prompts_dir, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                fallback_path = os.path.join(self.prompts_dir, 'default.txt')
                if os.path.exists(fallback_path):
                    with open(fallback_path, 'r', encoding='utf-8') as f:
                        return f.read().strip()
                else:
                    return "You are a helpful AI assistant."
        except Exception as e:
            print(f"Warning: Could not load prompt: {e}")
            return "You are a helpful AI assistant."
    
    def create_custom_prompt(self, prompt_id: str, name: str, description: str, content: str, category: str = "custom") -> bool:
        try:
            filename = f"{prompt_id}.txt"
            filepath = os.path.join(self.prompts_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.prompts[prompt_id] = {
                "name": name,
                "description": description,
                "file": filename,
                "category": category
            }
            
            self.save_config()
            return True
        except Exception as e:
            print(f"Error creating custom prompt: {e}")
            return False

prompt_manager = PromptManager()

class ChatbotConfig:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.temperature = 0.7
        self.max_tokens = 1000
        self.config_file = "config.json"
        self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.model = config_data.get('model', self.model)
                    self.temperature = config_data.get('temperature', self.temperature)
                    self.max_tokens = config_data.get('max_tokens', self.max_tokens)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        try:
            config_data = {
                'model': self.model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")

config = ChatbotConfig()

def load_system_prompt(prompt_id: Optional[str] = None):
    return prompt_manager.load_prompt_content(prompt_id)

def get_available_prompts():
    return prompt_manager.get_available_prompts()

def set_prompt(prompt_id: str) -> bool:
    return prompt_manager.set_prompt(prompt_id)

def get_current_prompt():
    return prompt_manager.get_current_prompt()

def create_custom_prompt(prompt_id: str, name: str, description: str, content: str, category: str = "custom") -> bool:
    return prompt_manager.create_custom_prompt(prompt_id, name, description, content, category)

def get_available_models():
    return AVAILABLE_MODELS

def set_model(model_name: str) -> bool:
    if model_name in AVAILABLE_MODELS:
        config.model = model_name
        config.save_config()
        return True
    return False

def get_current_model():
    return {
        'id': config.model,
        'info': AVAILABLE_MODELS.get(config.model, {})
    }

def ask_chatbot(messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
    try:
        model_to_use = model or config.model
        
        if model_to_use not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_to_use} not available")
        
        model_max_tokens = AVAILABLE_MODELS[model_to_use]["max_tokens"]
        effective_max_tokens = min(config.max_tokens, model_max_tokens)
        
        response = client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            temperature=config.temperature,
            max_tokens=effective_max_tokens
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def estimate_cost(messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, float]:
    model_to_use = model or config.model
    if model_to_use not in AVAILABLE_MODELS:
        return {"input": 0, "output": 0, "total": 0}
    
    input_chars = sum(len(msg["content"]) for msg in messages)
    input_tokens = input_chars / 4
    
    output_tokens = config.max_tokens / 2
    
    cost_info = AVAILABLE_MODELS[model_to_use]["cost_per_1k_tokens"]
    
    input_cost = (input_tokens / 1000) * cost_info["input"]
    output_cost = (output_tokens / 1000) * cost_info["output"]
    
    return {
        "input": round(input_cost, 6),
        "output": round(output_cost, 6),
        "total": round(input_cost + output_cost, 6)
    }

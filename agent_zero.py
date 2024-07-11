import os
import time
import random
import openai
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import yaml
import sys


# ---------------- Open and read the Prompt yaml file
with open('prompt.yaml', 'r') as file:
    data = yaml.safe_load(file)

# ----------------- Access the prompt and store it in a variable
prompt = data['prompt']

# ---------------- Print the prompt to verify
print("Loaded prompt:", prompt)

# ---------------- Ensure API keys are set in the environment
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
openai_api_key = os.environ.get('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("API key for OpenAI is not set in the environment variables.")

if not anthropic_api_key:
    raise ValueError("API key for Anthropic is not set in the environment variables.")

# Validate OpenAI API key format
if not openai_api_key.startswith('sk-'):
    raise ValueError("The OpenAI API key format is invalid. Please ensure it starts with 'sk-'.")

# Configure LLMs for different agents
openai_llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": openai_api_key
        }
    ],
    "temperature": 0.7,
}

# Configure Claude 3 using Autogen's config structure
claude_llm_config = {
    "config_list": [
        {
            "model": "claude-3-5-sonnet-20240620",
            "api_key": anthropic_api_key,
            "base_url": "http://localhost:4000/v1",
            "api_type": "openai"
        },
        {
            "model": "gpt-3.5-turbo",  # Fallback model
            "api_key": openai_api_key
        }
    ],
    "temperature": 0.7,
    "cache_seed": "44",
    "max_tokens": 4096
}

# Create agents
assistant_openai = AssistantAgent(
    name="assistant_openai", 
    llm_config=openai_llm_config,
    system_message="You are a helpful AI assistant. Respond to user queries and assist with tasks."
)
assistant_anthropic = AssistantAgent(
    name="assistant_anthropic", 
    llm_config=claude_llm_config,
    system_message="You are Claude, an AI assistant created by Anthropic. Help users with their queries and tasks."
)
code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=claude_llm_config,
    system_message="You are a code writing assistant. Help users write, debug, and improve their code.",
)

# Create UserProxyAgent with human input enabled
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=0,
    code_execution_config=False  # This disables code execution
)

# Create a group chat manager
groupchat = GroupChat(
    agents=[user_proxy, assistant_openai, assistant_anthropic, code_writer_agent], 
    messages=[], 
    max_round=12
)
manager = GroupChatManager(groupchat=groupchat, llm_config=openai_llm_config)

def exponential_backoff(attempt, max_attempts=5, base_delay=1):
    if attempt >= max_attempts:
        raise Exception("Maximum retry attempts reached")
    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1 * (2 ** attempt))
    time.sleep(delay)

# --------- Start a group chat with retry mechanism
max_attempts = 5
for attempt in range(max_attempts):
    try:
        user_proxy.initiate_chat(
            manager, 
            message=prompt
        )
        break 
    except openai.RateLimitError as e:
        print(f"Rate limit error occurred (attempt {attempt + 1}/{max_attempts}): {e}")
        if attempt < max_attempts - 1:
            print("Retrying with exponential backoff...")
            exponential_backoff(attempt)
        else:
            print("Max retry attempts reached. Please try again later.")
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        break  

print("Script execution completed.")
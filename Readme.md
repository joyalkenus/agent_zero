# Agent Zero
<div align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2hkNm1nanAzaTFsd2RoOW1tNHd1N2k2Yjh4aWN5NWF0OHJzczI2ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/CVtNe84hhYF9u/giphy.gif" width="500" />
</div>

Agent Zero is a project that i made for myself so as to improve the overall quality of the agentic system. This project demonstrates the use of multiple AI agents working together in a group chat environment. It utilizes OpenAI's GPT 4o model and Anthropic's Claude 3.5 sonnet model to create a collaborative AI system.

## Features

- Multiple AI agents: OpenAI assistant, Anthropic assistant (Claude), and a dedicated code writer agent (Currently configured to use claude)
- Group chat management for coordinating agent interactions
- Exponential backoff retry mechanism for handling rate limits
- YAML-based prompt configuration

*Note*: This execution asks for user input after each assistant speaks, you can turn this off by changing 
   ```human_input = "NEVER" ```

## Prerequisites

- Python 3.7+
- OpenAI API key
- Anthropic API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/agent-zero.git
   cd agent-zero
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```
   export OPENAI_API_KEY='your_openai_api_key_here'
   export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
   ```

## Usage

1. Prepare your prompt in a `prompt.yaml` file:
   ```yaml
   prompt: "Your prompt text here"
   ```

2. Run the main script:
   ```
   python agent_zero.py
   ```

## Configuration

- Modify the `openai_llm_config` and `claude_llm_config` dictionaries in `agent_zero.py` to adjust model parameters or API endpoints.
- The `GroupChat` is configured for a maximum of 12 rounds. Adjust the `max_round` parameter in the `GroupChat` initialization if needed.

## Troubleshooting

- If you encounter rate limit errors, the script will automatically retry with exponential backoff.
- Ensure that your API keys are correctly set in the environment variables.
- Check that the `prompt.yaml` file is in the same directory as the script and contains a valid prompt.

## Contributing

Contributions to Agent Zero are welcome! Please feel free to submit a Pull Request.


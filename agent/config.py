import os

# Read OpenAI API key from environment variable. Do NOT hardcode your key.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# Model name (change if you use another model)
MODEL = os.getenv("CLI_AGENT_MODEL", "gpt-4o-mini")

# Log file path
LOG_FILE = os.getenv("CLI_AGENT_LOG", "logs/agent_log.json")

# If SANDBOX is "1", commands will NOT be executed, only printed (safer for testing).
SANDBOX = os.getenv("CLI_AGENT_SANDBOX", "1") == "1"

# If AUTO_CONFIRM is "1", agent will auto-confirm potentially dangerous commands.
AUTO_CONFIRM = os.getenv("CLI_AGENT_AUTO_CONFIRM", "0") == "1"

# Project root for file writes (agent will not write outside this path)
PROJECT_ROOT = os.getenv("CLI_AGENT_PROJECT_ROOT", ".")

# LLM settings
DEFAULT_MODEL = "openai/gpt-oss-120b"
PARSER_TEMPERATURE = 0
JOBFIT_TEMPERATURE = 0.3
CRITIC_TEMPERATURE = 0
WRITER_TEMPERATURE = 0.4

# Workflow settings
MAX_RETRIES = 2

# File handling
SUPPORTED_RESUME_FORMATS = ["pdf", "docx", "txt"]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
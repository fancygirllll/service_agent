import os


MODEL = os.getenv("GOOGLE_GENAI_MODEL")
if not MODEL:
    MODEL = "gemini-1.5-flash-002"

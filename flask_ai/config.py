import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    HOST = os.getenv("HOST", "0.0.0.0")

    PORT = int(os.getenv("PORT", 5000))

    DEBUG = os.getenv("DEBUG", "True") == "True"

    SECRET_KEY = os.getenv("SECRET_KEY")

    MODEL_PATH = os.getenv("MODEL_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL")

import os
from dotenv import load_dotenv

def load_env_variables(env_path=".env"):
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        print(f" Environment loaded from {env_path}")
    else:
        print(" .env file not found")

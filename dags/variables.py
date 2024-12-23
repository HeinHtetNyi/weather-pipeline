import os
from dotenv import load_dotenv

load_dotenv()

class Variables:
    def __init__(self) -> None:
        self.API_KEY:str = os.getenv("API_KEY") or ""
        self.DB_URL:str = os.getenv("DB_URL") or ""

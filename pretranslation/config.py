from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY", "")
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1")
MOONSHOT_KEY = os.getenv("MOONSHOT_KEY", "")
SAKURA_URL = os.getenv("SAKURA_URL", "")
SAKURA_KEY = os.getenv("SAKURA_KEY", "114514")

def set_openai_key(key):
    global OPENAI_KEY
    OPENAI_KEY = key

def set_openai_url(url):
    global OPENAI_URL
    OPENAI_URL = url

def set_moonshot_key(key):
    global MOONSHOT_KEY
    MOONSHOT_KEY = key

def set_sakura_url(url):
    global SAKURA_URL
    SAKURA_URL = url

def set_sakura_key(key):
    global SAKURA_KEY
    SAKURA_KEY = key
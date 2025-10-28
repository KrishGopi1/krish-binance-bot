from dotenv import load_dotenv
from binance import Client
import os
import logging

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TESTNET = os.getenv("TESTNET", "True") == "True"

# Centralized logging configuration: write a single bot.log in the project root.
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot.log"))
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    filemode="a",
)

# Create the API client after logging is configured so modules can immediately log.
client = Client(API_KEY, API_SECRET, testnet=TESTNET)

try:
    server_time = client.get_server_time()
    print("Connected", server_time)
except Exception as e:
    print("Failed Connection", e)

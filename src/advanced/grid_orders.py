from src.limit_orders import place_limit_order
import logging, os, numpy as np
from src.config import client

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log")
logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.FileHandler(LOG_FILE, mode="a")
    f = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    h.setFormatter(f)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

def validate_symbol(symbol: str):
    try:
        info = client.futures_exchange_info()
        symbols = {s["symbol"]: s for s in info["symbols"]}
        if symbol not in symbols:
            print(f"Invalid symbol: {symbol}")
            return None
        return symbols[symbol]
    except Exception as e:
        print("Failed to fetch symbol info:", e)
        return None

def grid(symbol, side, qty, lower, upper, levels=5):
    symbol = symbol.upper()
    meta = validate_symbol(symbol)
    if not meta:
        return
    if upper <= lower or levels < 2:
        print("Invalid grid range or levels.")
        return
    price_filter = next(f for f in meta["filters"] if f["filterType"] == "PRICE_FILTER")
    tick_size = float(price_filter["tickSize"])
    min_price = float(price_filter["minPrice"])
    max_price = float(price_filter["maxPrice"])

    prices = np.linspace(lower, upper, levels)
    print(f"Setting {levels} {side} limit orders between {lower} and {upper}")
    for p in prices:
        if not (min_price <= p <= max_price):
            print(f"Skipping {p}: out of range ({min_price}–{max_price})")
            continue
        p = round(p / tick_size) * tick_size
        place_limit_order(symbol, side, qty, p)
        logger.info(f"GRID {side} {symbol} qty={qty} price={p}")
    print("Grid placed successfully!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Grid order placer")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity", type=float)
    parser.add_argument("--lower", type=float, required=True)
    parser.add_argument("--upper", type=float, required=True)
    parser.add_argument("--levels", type=int, default=5)
    args = parser.parse_args()
    grid(args.symbol, args.side, args.quantity, args.lower, args.upper, args.levels)

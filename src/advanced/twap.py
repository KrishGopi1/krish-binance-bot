from src.market_orders import place_market_order
import logging, os, time
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

def twap(symbol, side, total_qty, slices=5, interval=5):
    symbol = symbol.upper()
    meta = validate_symbol(symbol)
    if not meta:
        return
    if slices <= 0 or total_qty <= 0 or interval < 1:
        print("Invalid TWAP parameters.")
        return
    slice_qty = total_qty / slices
    print(f"Executing TWAP: {slices} slices of {slice_qty} every {interval}s")
    for i in range(slices):
        print(f"Slice {i+1}/{slices}")
        place_market_order(symbol, side, slice_qty)
        logger.info(f"TWAP {side} {symbol} slice={i+1}/{slices} qty={slice_qty}")
        if i < slices - 1:
            time.sleep(interval)
    print("TWAP complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TWAP order executor")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity", type=float)
    parser.add_argument("--slices", type=int, default=5)
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()
    twap(args.symbol, args.side, args.quantity, args.slices, args.interval)

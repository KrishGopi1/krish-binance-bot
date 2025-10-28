from src.config import client
import logging, os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log")
logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.FileHandler(LOG_FILE, mode="a")
    f = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    h.setFormatter(f)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

def validate_symbol(symbol):
    try:
        info = client.futures_exchange_info()
        if symbol not in [s["symbol"] for s in info["symbols"]]:
            print(f"Invalid symbol: {symbol}")
            return False
        return True
    except Exception as e:
        print("Failed to fetch symbol info:", e)
        return False

def place_oco(symbol, side, qty, tp_price, sl_price):
    symbol = symbol.upper()
    if not validate_symbol(symbol):
        return
    opp = "SELL" if side.upper() == "BUY" else "BUY"
    try:
        print(f"Placing OCO pair for {symbol}: TP={tp_price}, SL={sl_price}")
        tp = client.futures_create_order(
            symbol=symbol, side=opp, type="TAKE_PROFIT_MARKET",
            stopPrice=str(tp_price), reduceOnly=True, quantity=qty
        )
        sl = client.futures_create_order(
            symbol=symbol, side=opp, type="STOP_MARKET",
            stopPrice=str(sl_price), reduceOnly=True, quantity=qty
        )
        print("OCO orders created.")
        logger.info(f"OCO {symbol} TP={tp_price} SL={sl_price} qty={qty}")
    except Exception as e:
        print("OCO failed:", e)
        logger.error(f"OCO failed {symbol}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Manual OCO for Binance Futures")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity", type=float)
    parser.add_argument("--tp", type=float, required=True)
    parser.add_argument("--sl", type=float, required=True)
    args = parser.parse_args()
    place_oco(args.symbol, args.side, args.quantity, args.tp, args.sl)

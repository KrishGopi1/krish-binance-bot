from src.config import client
import logging

logger = logging.getLogger(__name__)

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

def place_market_order(symbol: str, side: str, quantity: float):
    symbol = symbol.upper()
    meta = validate_symbol(symbol)
    if not meta:
        return
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        print("Invalid side! Use BUY or SELL.")
        return

    try:
        print(f"Placing {side} MARKET order for {quantity} {symbol}...")
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        print("Order successful!")
        print("Order ID:", order["orderId"])
        print("Avg Price:", order["avgPrice"])
        print("Executed Qty:", order["executedQty"])
        logger.info(f"{side} MARKET {symbol} qty={quantity}")
    except Exception as e:
        print("Order failed:", e)
        logger.error(f"MARKET order failed for {symbol}: {e}")

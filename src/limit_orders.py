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

def place_limit_order(symbol: str, side: str, quantity: float, price: float, time_in_force="GTC"):
    symbol = symbol.upper()
    meta = validate_symbol(symbol)
    if not meta:
        return
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        print("Invalid side! Use BUY or SELL.")
        return
    if quantity <= 0 or price <= 0:
        print("Quantity or price is invalid")
        return

    try:
        print(f"Placing {side} LIMIT order for {quantity} {symbol} @ {price}...")
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce=time_in_force,
            quantity=quantity,
            price=price
        )
        print("Limit order placed successfully!")
        print("Order ID:", order["orderId"])
        print("Status:", order["status"])
        logger.info(f"{side} LIMIT {symbol} qty={quantity} price={price}")
    except Exception as e:
        print("Order failed:", e)
        logger.error(f"LIMIT order failed for {symbol}: {e}")

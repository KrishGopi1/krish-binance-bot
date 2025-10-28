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

def place_stop_limit_order(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float, time_in_force="GTC"):
    symbol = symbol.upper()
    meta = validate_symbol(symbol)
    if not meta:
        return
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        print("Invalid side (BUY/SELL only)")
        return
    if quantity <= 0 or stop_price <= 0 or limit_price <= 0:
        print("Quantity and prices must be positive.")
        return
    if side == "BUY" and stop_price >= limit_price:
        print("For BUY STOP-LIMIT: stop price must be < limit price.")
        return
    if side == "SELL" and stop_price <= limit_price:
        print("For SELL STOP-LIMIT: stop price must be > limit price.")
        return


    try:
        print(f"Placing {side} STOP-LIMIT order for {symbol}: qty={quantity}, stop={stop_price}, limit={limit_price}")
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=str(stop_price),
            price=str(limit_price),
            timeInForce=time_in_force
        )
        print("STOP-LIMIT order placed successfully!")
        logger.info(f"{side} STOP-LIMIT {symbol} qty={quantity} stop={stop_price} limit={limit_price}")
    except Exception as e:
        print("Order failed:", e)
        logger.error(f"STOP-LIMIT order failed for {symbol}: {e}")

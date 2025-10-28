import argparse
import logging, os
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.stop_limit_orders import place_stop_limit_order
from src.advanced.oco import place_oco
from src.advanced.twap import twap
from src.advanced.grid_orders import grid

LOG_FILE = os.path.join(os.path.dirname(__file__), "bot.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
for h in logger.handlers[:]:
    logger.removeHandler(h)
fh = logging.FileHandler(LOG_FILE, mode="a")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def main():
    parser = argparse.ArgumentParser(description="Unified Binance Futures Bot CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    mkt = sub.add_parser("market", help="Place market order")
    mkt.add_argument("symbol")
    mkt.add_argument("side")
    mkt.add_argument("quantity", type=float)

    lim = sub.add_parser("limit", help="Place limit order")
    lim.add_argument("symbol")
    lim.add_argument("side")
    lim.add_argument("quantity", type=float)
    lim.add_argument("--price", type=float, required=True)
    lim.add_argument("--tif", type=str, default="GTC")

    stp = sub.add_parser("stoplimit", help="Place stop-limit order")
    stp.add_argument("symbol")
    stp.add_argument("side")
    stp.add_argument("quantity", type=float)
    stp.add_argument("--stop", type=float, required=True)
    stp.add_argument("--limit", type=float, required=True)

    oco_p = sub.add_parser("oco", help="Place OCO orders")
    oco_p.add_argument("symbol")
    oco_p.add_argument("side")
    oco_p.add_argument("quantity", type=float)
    oco_p.add_argument("--tp", type=float, required=True)
    oco_p.add_argument("--sl", type=float, required=True)

    tw = sub.add_parser("twap", help="Execute TWAP orders")
    tw.add_argument("symbol")
    tw.add_argument("side")
    tw.add_argument("quantity", type=float)
    tw.add_argument("--slices", type=int, default=5)
    tw.add_argument("--interval", type=int, default=5)

    grd = sub.add_parser("grid", help="Place grid limit orders")
    grd.add_argument("symbol")
    grd.add_argument("side")
    grd.add_argument("quantity", type=float)
    grd.add_argument("--lower", type=float, required=True)
    grd.add_argument("--upper", type=float, required=True)
    grd.add_argument("--levels", type=int, default=5)

    args = parser.parse_args()

    if args.command == "market":
        place_market_order(args.symbol, args.side, args.quantity)
    elif args.command == "limit":
        place_limit_order(args.symbol, args.side, args.quantity, args.price, args.tif)
    elif args.command == "stoplimit":
        place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop, args.limit)
    elif args.command == "oco":
        place_oco(args.symbol, args.side, args.quantity, args.tp, args.sl)
    elif args.command == "twap":
        twap(args.symbol, args.side, args.quantity, args.slices, args.interval)
    elif args.command == "grid":
        grid(args.symbol, args.side, args.quantity, args.lower, args.upper, args.levels)

if __name__ == "__main__":
    main()

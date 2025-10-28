# Binance Futures Trading Bot (Testnet)

### Developer: **Krish Gopi**


---

## Overview

This repository contains a **Python-based Binance USDT-M Futures Trading Bot**, built for the **Binance Futures Testnet** using the official [`python-binance`](https://github.com/sammchardy/python-binance) library.  
It supports multiple order types with robust **validation**, **error handling**, and **logging**.

The bot is **CLI-driven**, making it lightweight, easily scriptable, and suitable for professional trading automation.

---

## Features

| Category | Supported Orders | Description |
|-----------|------------------|--------------|
| **Core** | Market Orders | Executes immediately at market price |
|  | Limit Orders | Executes at a specified limit price |
| **Advanced** | Stop-Limit Orders | Triggered limit order after stop price is hit |
|  | OCO (One Cancels the Other) | Simulated manually using two linked orders |
|  | TWAP | Splits large orders into multiple timed slices |
|  | Grid Orders | Places limit orders at equally spaced prices |

---

## Project Structure

```
TradingBot/
│
├── src/
│   ├── bot.py                # Unified CLI entry point
│   ├── config.py             # Loads .env and initializes Binance Client
│   ├── market_orders.py      # Handles market order logic
│   ├── limit_orders.py       # Handles limit order logic
│   ├── advanced/
│       ├── stop_limit_orders.py
│       ├── oco.py
│       ├── twap.py
│       ├── grid_orders.py
│
├── .env                      # Environment variables (excluded from repo)
├── requirements.txt
├── README.md
└── bot.log                   # Log file for trades and errors
```

---

##   Installation

### Clone Repository
```bash
git clone https://github.com/<your-username>/Binance-Futures-Bot.git
cd Binance-Futures-Bot
```

### Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
TESTNET=True
```

> Use Binance **Futures Testnet** credentials.  
> Testnet URL: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

---

## 💻 Usage

Each command corresponds to a different order type.  
Use:
```bash
python -m src.bot <command> <symbol> <side> <quantity> [additional arguments]
```

### Example Commands
#### Market Order
```bash
python -m src.bot market BTCUSDT BUY 0.001
```

#### Limit Order
```bash
python -m src.bot limit BTCUSDT SELL 0.001 --price 70000
```

#### Stop-Limit Order
```bash
python -m src.bot stoplimit BTCUSDT BUY 0.001 --stop 66000 --limit 65900
```

#### TWAP (Time Weighted Average Price)
```bash
python -m src.bot twap BTCUSDT BUY 0.01 --slices 5 --interval 5
```

#### Grid Orders
```bash
python -m src.bot grid BTCUSDT SELL 0.001 --lower 64000 --upper 66000 --levels 5
```

#### OCO (Manual Implementation)
```bash
python -m src.bot oco BTCUSDT SELL 0.001 --stop 65000 --limit 65100
```

---

## Validation & Error Handling

All inputs undergo strict validation before calling the Binance API:
- Validates **symbol existence** via `futures_exchange_info()`
- Confirms **order side** (`BUY` / `SELL`)
- Ensures **positive price and quantity**
- Verifies **stop vs limit** relationships
- Handles API exceptions gracefully with error messages

---

## Logging

All actions and errors are written to `src/bot.log`.

Example:
```
2025-10-28 22:31:22 [INFO] src.market_orders - BUY MARKET BTCUSDT qty=0.001 id=7580408421
2025-10-28 22:32:05 [ERROR] src.stop_limit_orders - STOP-LIMIT order failed for BTCUSDT: Price out of range
```

---

## Design Decisions

| Choice | Reason |
|--------|--------|
| **Unified CLI Interface** | Portable, scriptable, easy to debug |
| **Manual OCO** | Futures Testnet lacks native OCO endpoint |
| **Centralized Logging** | Ensures consistent format and unified audit trail |
| **Separate Modules** | Easier to test and extend each order type independently |

---a

## Testing

More than **50 test cases** were executed, including:
- Order placement success/failure
- Input validation (invalid symbol, side, price, etc.)
- TWAP slice timing and logging verification
- Stop-limit condition tests
- OCO manual trigger simulation

Logs and screenshots available in `/src/bot.log`.

---

## 🧰 Requirements

- Python 3.10+
- `python-binance`
- `python-dotenv`
- `numpy`
- `argparse`

Install via:
```bash
pip install -r requirements.txt
```


---

## References

- [Binance Futures API Docs](https://binance-docs.github.io/apidocs/futures/en/)
- [python-binance GitHub Repository](https://github.com/sammchardy/python-binance)
- [Binance Testnet](https://testnet.binancefuture.com)

---

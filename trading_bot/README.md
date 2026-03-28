# Binance Futures Testnet — Trading Bot

A small CLI tool to place orders on Binance Futures Testnet (USDT-M). Supports Market, Limit, and Stop-Market orders with structured logging and input validation.

---

## Setup

**1. Clone and install dependencies**
```bash
git clone <your-repo-url>
cd trading_bot
pip install -r requirements.txt
```

**2. Get your API credentials**

- Register at [testnet.binancefuture.com](https://testnet.binancefuture.com)
- Go to API Management → Generate API key & secret

**3. Export credentials as environment variables**
```bash
export BINANCE_API_KEY=your_api_key_here
export BINANCE_API_SECRET=your_api_secret_here
```

> On Windows (cmd): use `set` instead of `export`

---

## How to Run

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit Order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3450
```

### Stop-Market Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 65000
```

### More verbose console output
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --log-level DEBUG
```

---

## Example Output

```
────────────────────────────────────────────
  ORDER REQUEST
────────────────────────────────────────────
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.01
────────────────────────────────────────────
  ORDER RESPONSE
────────────────────────────────────────────
  Order ID  : 3921748302
  Status    : FILLED
  Exec Qty  : 0.010
  Avg Price : 67843.20
  Client OID: web_xKp3RnmT7Qv21oYzF8Ls
────────────────────────────────────────────
  ✓ Order placed successfully!

  Log saved to: logs/trading_bot_2025-06-04.log
```

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST client (signing, HTTP)
│   ├── orders.py          # order placement + output formatting
│   ├── validators.py      # input validation, decoupled from CLI
│   └── logging_config.py  # file + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # auto-created on first run
├── requirements.txt
└── README.md
```

---

## Logging

Logs are written to `logs/trading_bot_YYYY-MM-DD.log` automatically. Each file contains:
- All API request parameters (minus the signature)
- Full API responses
- Validation errors and network failures

Console output is INFO-level by default to avoid noise. Use `--log-level DEBUG` to see request/response details in the terminal too.

---

## Assumptions

- Only USDT-M futures are supported (testnet URL is hardcoded to `https://testnet.binancefuture.com`)
- `timeInForce` defaults to `GTC` for Limit orders — didn't add a flag for it since GTC is the sensible default for most use cases
- Quantity precision isn't validated client-side; Binance will reject with a clear error if the precision is wrong for the symbol
- Credentials are expected via environment variables rather than a config file to avoid accidentally committing secrets

---

## Dependencies

- `requests` — HTTP client for REST calls. Chose this over `python-binance` to keep the dependency footprint minimal and make the API interaction transparent.

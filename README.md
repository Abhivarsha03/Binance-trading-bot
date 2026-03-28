# Binance Futures Trading Bot (Testnet)

## Overview

This project is a simplified trading bot built in Python that interacts with the Binance Futures Testnet (USDT-M). It allows users to place MARKET and LIMIT orders through a command-line interface (CLI) with proper validation, logging, and structured code design.

The goal of this project is to demonstrate clean architecture, API integration, and robust error handling in a real-world trading scenario.

---

## Features

* Place **MARKET** and **LIMIT** orders
* Supports both **BUY** and **SELL** operations
* Command-line interface using argparse
* Input validation with clear error messages
* Structured codebase (separation of concerns)
* Logging of API requests, responses, and errors
* Works with Binance Futures **Testnet** (safe for testing)

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py        # Binance API client
│   ├── orders.py        # Order execution logic
│   ├── validators.py    # Input validation
│   ├── logger.py        # Logging configuration
│
├── cli.py               # CLI entry point
├── requirements.txt
├── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/Abhivarsha03/Binance-trading-bot.git
cd Binance-trading-bot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure API credentials

Create a `.env` file in the root directory:

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret_key
```

Make sure you are using **Binance Futures Testnet credentials**, not live keys.

---

## Usage

### MARKET Order Example

```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT Order Example

```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

---

## Sample Output

```
=== ORDER SUMMARY ===
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001

=== RESPONSE ===
Order ID: 12345678
Status: FILLED
Executed Quantity: 0.001
Average Price: 59850.12
```

---

## Logging

All API interactions and errors are logged to a file:

```
trading_bot.log
```

Logs include:

* Request parameters
* API responses
* Error messages

### Example Log Entry

```
INFO - Sending order: {'symbol': 'BTCUSDT', 'side': 'BUY', ...}
INFO - Response: {'orderId': 12345678, 'status': 'FILLED'}
ERROR - API error: Invalid quantity
```

---

## Validation

The application validates:

* Order side (BUY/SELL)
* Order type (MARKET/LIMIT)
* Quantity (> 0)
* Price requirement for LIMIT orders

Clear error messages are provided for invalid inputs.

---

## Assumptions

* Only USDT-M Futures Testnet is used
* User provides valid trading symbols (e.g., BTCUSDT)
* Internet connection is stable for API calls

---

## Notes

* This project is intended for **testing and demonstration purposes only**
* It does not include advanced trading strategies or risk management
* Do NOT use real API keys

---

## Future Improvements

* Add Stop-Limit or OCO order support
* Improve CLI UX with interactive prompts
* Add retry mechanism for API failures
* Extend logging with structured formats (JSON)

---

## Author

Developed as part of a Python Developer Internship assignment.

---

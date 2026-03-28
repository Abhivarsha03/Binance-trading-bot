#!/usr/bin/env python3
"""
Trading bot CLI — Binance Futures Testnet

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2000
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 58000
"""

import argparse
import os
import sys
import logging

from bot.logging_config import setup_logging
from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.validators import validate_order_inputs, ValidationError
from bot.orders import place_order, format_order_summary, format_order_response

logger = logging.getLogger(__name__)


def get_credentials():
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print(
            "\n[ERROR] API credentials not found.\n"
            "Please set BINANCE_API_KEY and BINANCE_API_SECRET as environment variables.\n"
            "  export BINANCE_API_KEY=your_key\n"
            "  export BINANCE_API_SECRET=your_secret\n"
        )
        sys.exit(1)

    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    p.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order direction")
    p.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        help="Order type",
    )
    p.add_argument("--quantity", required=True, help="Order quantity")
    p.add_argument("--price", default=None, help="Limit price (required for LIMIT orders)")
    p.add_argument("--stop-price", dest="stop_price", default=None, help="Stop price (required for STOP_MARKET)")
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING"],
        help="Console log verbosity (default: INFO)",
    )
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    log_file = setup_logging(log_level=args.log_level)

    logger.debug("Starting trading bot | args=%s", vars(args))

    try:
        params = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as e:
        print(f"\n[VALIDATION ERROR] {e}\n")
        logger.warning("Validation failed: %s", e)
        sys.exit(1)

    print(format_order_summary(params))

    api_key, api_secret = get_credentials()
    client = BinanceClient(api_key, api_secret)

    try:
        response = place_order(client, params)
        print(format_order_response(response))
        print("  ✓ Order placed successfully!\n")
    except BinanceAPIError as e:
        code_info = f" (code {e.code})" if e.code else ""
        print(f"\n[API ERROR{code_info}] {e}\n")
        logger.error("Order failed with API error: %s", e)
        sys.exit(1)
    except NetworkError as e:
        print(f"\n[NETWORK ERROR] {e}\n")
        logger.error("Network error: %s", e)
        sys.exit(1)

    print(f"  Log saved to: {log_file}\n")


if __name__ == "__main__":
    main()

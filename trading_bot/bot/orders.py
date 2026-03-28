import logging
from bot.client import BinanceClient

logger = logging.getLogger(__name__)


def place_order(client: BinanceClient, params: dict) -> dict:
    """
    Sends the order to Binance and returns the response dict.
    Caller is responsible for validated params (see validators.py).
    """
    logger.info(
        "Placing %s %s order | symbol=%s qty=%s%s",
        params["side"],
        params["type"],
        params["symbol"],
        params["quantity"],
        f" price={params['price']}" if "price" in params else "",
    )

    # Build the payload — quantity key is 'quantity' in our internal dict
    # but Binance expects it as 'quantity' too, so just pass it through.
    payload = {k: v for k, v in params.items()}

    response = client.place_order(**payload)

    logger.info(
        "Order accepted | orderId=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice", "N/A"),
    )

    return response


def format_order_summary(params: dict) -> str:
    lines = [
        "─" * 44,
        "  ORDER REQUEST",
        "─" * 44,
        f"  Symbol    : {params['symbol']}",
        f"  Side      : {params['side']}",
        f"  Type      : {params['type']}",
        f"  Quantity  : {params['quantity']}",
    ]
    if "price" in params:
        lines.append(f"  Price     : {params['price']}")
    if "stopPrice" in params:
        lines.append(f"  Stop Price: {params['stopPrice']}")
    lines.append("─" * 44)
    return "\n".join(lines)


def format_order_response(resp: dict) -> str:
    lines = [
        "  ORDER RESPONSE",
        "─" * 44,
        f"  Order ID  : {resp.get('orderId')}",
        f"  Status    : {resp.get('status')}",
        f"  Exec Qty  : {resp.get('executedQty')}",
        f"  Avg Price : {resp.get('avgPrice', 'N/A')}",
        f"  Client OID: {resp.get('clientOrderId', 'N/A')}",
        "─" * 44,
    ]
    return "\n".join(lines)

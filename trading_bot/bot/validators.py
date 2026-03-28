"""
Input validation helpers.
Kept separate so the CLI layer stays clean and validators can be
unit-tested without spinning up an actual API connection.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValidationError("Symbol cannot be empty.")
    # basic sanity — Binance futures pairs are all alpha
    if not s.isalpha():
        raise ValidationError(f"Symbol '{s}' looks off — expected something like BTCUSDT.")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(f"Side must be one of {VALID_SIDES}, got '{side}'.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be one of {VALID_ORDER_TYPES}, got '{order_type}'.")
    return t


def validate_quantity(qty: str) -> float:
    try:
        val = float(qty)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a number, got '{qty}'.")
    if val <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return val


def validate_price(price: str) -> float:
    try:
        val = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Price must be a number, got '{price}'.")
    if val <= 0:
        raise ValidationError("Price must be greater than 0.")
    return val


def validate_order_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Run all validations and return a cleaned dict ready to pass to the API.
    Raises ValidationError on the first problem found.
    """
    result = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
    }

    if result["type"] == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        result["price"] = validate_price(price)
        result["timeInForce"] = "GTC"  # sensible default

    if result["type"] == "STOP_MARKET":
        if stop_price is None:
            raise ValidationError("--stop-price is required for STOP_MARKET orders.")
        result["stopPrice"] = validate_price(stop_price)

    return result

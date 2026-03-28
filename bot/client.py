import hashlib
import hmac
import time
import logging
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = f"{BASE_URL}{endpoint}"

        logger.debug("POST %s | params: %s", url, {k: v for k, v in signed.items() if k != "signature"})

        try:
            resp = self.session.post(url, data=signed, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            logger.debug("Response: %s", data)
            return data
        except requests.exceptions.HTTPError as e:
            # Binance sends error details in response body even on 4xx
            try:
                err_body = e.response.json()
                logger.error("API error %s: %s", e.response.status_code, err_body)
                raise BinanceAPIError(err_body.get("msg", str(e)), err_body.get("code")) from e
            except ValueError:
                raise BinanceAPIError(str(e)) from e
        except requests.exceptions.ConnectionError as e:
            logger.error("Network error: %s", e)
            raise NetworkError("Could not reach Binance testnet. Check your connection.") from e
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise NetworkError("Request timed out.")

    def _get(self, endpoint: str, params: dict = None) -> dict:
        params = params or {}
        signed = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.debug("GET %s | params: %s", url, {k: v for k, v in signed.items() if k != "signature"})

        try:
            resp = self.session.get(url, params=signed, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            try:
                err_body = e.response.json()
                logger.error("API error: %s", err_body)
                raise BinanceAPIError(err_body.get("msg", str(e)), err_body.get("code")) from e
            except ValueError:
                raise BinanceAPIError(str(e)) from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError("Could not reach Binance testnet.") from e

    def place_order(self, **kwargs) -> dict:
        return self._post("/fapi/v1/order", kwargs)

    def get_exchange_info(self) -> dict:
        # no auth needed but we still reuse session
        url = f"{BASE_URL}/fapi/v1/exchangeInfo"
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()


class BinanceAPIError(Exception):
    def __init__(self, message: str, code: int = None):
        self.code = code
        super().__init__(message)


class NetworkError(Exception):
    pass

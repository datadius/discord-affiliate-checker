import requests
from os import getenv
import hmac
import hashlib
import time
import orjson


class CoinbaseImpact:
    def __init__(self):
        self.base_url = "https://api.mexc.com"
        self.api_key = getenv("MEXC_API_KEY")
        self.api_secret = getenv("MEXC_API_SECRET")

    def get_exchange_name(self):
        return "Coinbase"


if __name__ == "__main__":
    pass

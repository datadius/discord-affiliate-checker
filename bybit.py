import requests
from os import getenv
import hmac
import hashlib
import time
import orjson


class Bybit:
    def __init__(self):
        self.base_url = "https://api.bybit.com"
        self.api_key = getenv("BYBIT_API_KEY")
        self.api_secret = getenv("BYBIT_API_SECRET")

    def generate_headers(self, payload, api_key, api_secret, recv_window=5000):
        # recvWindow, may be sent to specify the number of milliseconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
        # Serious trading is about timing. Networks can be unstable and unreliable, which can lead to requests taking varying amounts of time to reach the servers. With recvWindow, you can specify that the request must be processed within a certain number of milliseconds or be rejected by the server.
        timestamp = int(time.time() * 1000)
        sign = self._auth(api_key, api_secret, payload, recv_window, timestamp)
        return {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": sign,
            "X-BAPI-TIMESTAMP": str(timestamp),
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-RECV-WINDOW": str(recv_window),
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }

    def _auth(self, api_key, api_secret, payload, recv_window, timestamp):
        """
        Generates authentication signature per Bybit API specifications.
        """

        def generate_hmac():
            hash = hmac.new(
                bytes(api_secret, "utf-8"),
                param_str.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        if api_key is None or api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_str = str(timestamp) + api_key + str(recv_window) + payload

        return generate_hmac()

    def get_uid_info(self, uid, value=100):
        endpoint = "/v5/user/aff-customer-info"
        params = f"uid={uid}"
        headers = self.generate_headers(params, self.api_key, self.api_secret)
        r = requests.get(f"{self.base_url}{endpoint}?{params}", headers=headers)

        user_info = orjson.loads(r.text)["result"]

        if (
            user_info.get("totalWalletBalance") is not None
            and user_info.get("uid") is not None
        ):
            balance = int(user_info.get("totalWalletBalance").partition(".")[0])
            value = self.convert_value_to_total_wallet_balance(value)
            depositLast365 = int(user_info.get("depositAmount365Day").partition(".")[0])

            return (
                balance > value,
                depositLast365,
                True,
            )
        elif user_info.get("uid") is not None:
            return False, 0, True

        return False, 0, False

    def get_exchange_name(self):
        return "Bybit"

    def convert_value_to_total_wallet_balance(self, value):
        if value < 100:
            return 1
        elif value >= 100 and value < 250:
            return 2
        elif value >= 250 and value < 500:
            return 3
        else:
            return 4


if __name__ == "__main__":
    bybit = Bybit()
    print("(True, 16190, True) ", bybit.get_uid_info("49938035"))
    print("(False, 0, False) ", bybit.get_uid_info("49933035"))
    print("(False, 0, True) ", bybit.get_uid_info("49938035", value=1000))

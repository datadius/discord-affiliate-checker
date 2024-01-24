import requests
from os import getenv
import time
import hmac
import hashlib
from math import trunc


class Phemex:
    def __init__(self):
        self.base_url = "https://api.phemex.com"
        self.api_key = getenv("PHEMEX_API_KEY")
        self.api_secret = getenv("PHEMEX_API_SECRET")

    def get_uid_info(self, uid):
        endpoint = "/api/referral/list"
        headers = self.generate_headers(endpoint)
        print(headers)
        r = requests.get(self.base_url + endpoint, headers=headers)
        print(r.text)
        # check if uid is in the list

    def generate_headers(self, endpoint, recv_window=60):
        # recvWindow, may be sent to specify the number of seconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
        # Serious trading is about timing. Networks can be unstable and unreliable, which can lead to requests taking varying amounts of time to reach the servers. With recvWindow, you can specify that the request must be processed within a certain number of milliseconds or be rejected by the server.
        timestamp = str(trunc(time.time()) + recv_window)
        sign = self._auth(endpoint, timestamp)
        return {
            "x-phemex-request-signature": sign,
            "x-phemex-request-expiry": timestamp,
            "x-phemex-access-token": self.api_key,
            "Content-Type": "application/json",
        }

    def _auth(self, endpoint, timestamp):
        """
        Generates authentication signature per Phemex API specifications.
        """

        def generate_hmac():
            hash = hmac.new(
                self.api_secret.encode("utf-8"),
                param_str.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_str = endpoint + timestamp
        print(param_str)

        return generate_hmac()


if __name__ == "__main__":
    phemex = Phemex()
    phemex.get_uid_info("100480")

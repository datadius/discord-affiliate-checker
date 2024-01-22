import requests
from os import getenv
import time
import hmac
import hashlib


class Fairdesk:
    def __init__(self):
        self.base_url = "https://api.fairdesk.com"
        self.api_key = getenv("FAIRDESK_API_KEY")
        self.api_secret = getenv("FAIRDESK_API_SECRET")

    def get_uid_info(self, uid):
        payload = f"/api/v1/private/account/partner-direct-user-deposit?traderUid={uid}"
        headers = self.generate_headers(payload)
        r = requests.get(self.base_url + payload, headers=headers)
        print(r.text)

    def generate_headers(self, payload, recv_window=5000):
        # recvWindow, may be sent to specify the number of milliseconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
        # Serious trading is about timing. Networks can be unstable and unreliable, which can lead to requests taking varying amounts of time to reach the servers. With recvWindow, you can specify that the request must be processed within a certain number of milliseconds or be rejected by the server.
        timestamp = int(time.time() * 1000)
        sign = self._auth(payload, recv_window, timestamp)
        return {
            "X-FAIRDESK-ACCESS-KEY": self.api_key,
            "X-FAIRDESK-REQUEST-SIGNATURE": sign,
            "X-FAIRDESK-REQUEST-EXPIRY": str(timestamp + recv_window),
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }

    def _auth(self, payload, recv_window, timestamp):
        """
        Generates authentication signature per Bybit API specifications.
        """

        def generate_hmac():
            hash = hmac.new(
                bytes(self.api_secret, "utf-8"),
                param_str.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        param_str = payload + str(timestamp + recv_window)

        return generate_hmac()


if __name__ == "__main__":
    fairdesk = Fairdesk()
    fairdesk.get_uid_info("100480")

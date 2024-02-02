import requests
from os import getenv
import time
import hmac
import hashlib
from math import trunc
import orjson


class Phemex:
    def __init__(self):
        self.base_url = "https://api-3rd.phemex.com"
        self.api_key = getenv("PHEMEX_API_KEY")
        self.api_secret = getenv("PHEMEX_API_SECRET")

    def get_uid_info(self, uid, value=100):
        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")
        endpoint = "/api/referral/deposits"
        query = "pageSize=100&pageNum=1"
        headers = self.generate_headers(endpoint, query)
        r = requests.get(self.base_url + endpoint + "?" + query, headers=headers)
        response_json = orjson.loads(r.text)
        total = response_json["data"]["total"]
        response_list = response_json["data"]["rows"]
        if int(total) > 100:
            for index in range(100):
                if (
                    response_list[index]["userId"] == uid
                    and response_list[index]["depositsRv"] >= value
                ):
                    return True

            for page in range(2, int(total / 100) + 1):
                query = f"pageSize=100&pageNum={page}"
                headers = self.generate_headers(endpoint, query)
                r = requests.get(
                    self.base_url + endpoint + "?" + query, headers=headers
                )
                response_json = orjson.loads(r.text)
                response_list = response_json["data"]["rows"]
                for index in range(100):
                    if (
                        response_list[index]["userId"] == uid
                        and response_list[index]["depositsRv"] >= value
                    ):
                        return True
        else:
            for index in range(len(response_list)):
                if (
                    response_list[index]["userId"] == uid
                    and response_list[index]["depositsRv"] >= value
                ):
                    return True
        return False

    def generate_headers(self, endpoint, query="", recv_window=60):
        # recvWindow, may be sent to specify the number of seconds after timestamp the request is valid for. If recvWindow is not sent, it defaults to 5000.
        # Serious trading is about timing. Networks can be unstable and unreliable, which can lead to requests taking varying amounts of time to reach the servers. With recvWindow, you can specify that the request must be processed within a certain number of milliseconds or be rejected by the server.
        timestamp = str(trunc(time.time()) + recv_window)
        sign = self._auth(endpoint, query, timestamp)
        return {
            "x-phemex-request-signature": sign,
            "x-phemex-request-expiry": timestamp,
            "x-phemex-access-token": self.api_key,
            "Content-Type": "application/json",
        }

    def _auth(self, endpoint, query, timestamp):
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

        param_str = endpoint + query + timestamp

        return generate_hmac()

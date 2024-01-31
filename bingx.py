import requests
from os import getenv
import hmac
import hashlib
import time


class BingX:
    def __init__(self):
        self.base_url = "https://open-api.bingx.com"
        self.api_key = getenv("BINGX_API_KEY")
        self.api_secret = getenv("BINGX_API_SECRET")

    def get_uid_info(self, uid, value=100):
        endpoint = "/openApi/agent/v1/asset/depositDetailLlist"
        params = (
            f"uid={uid}&bizType=1&recvWindow=5000&timestamp={int(time.time() * 1000)}"
        )
        params = self._auth(params)
        r = requests.get(
            f"{self.base_url}{endpoint}?{params}", headers={"X-BX-APIKEY": self.api_key}
        )
        print(r.text)
        # check if uid is in the list

    def _auth(self, params):
        """
        Generates authentication signature per Phemex API specifications.
        """

        def generate_hmac():
            hash = hmac.new(
                self.api_secret.encode("utf-8"),
                params.encode("utf-8"),
                hashlib.sha256,
            )
            return f"{params}&signature={hash.hexdigest()}"

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        return generate_hmac()


if __name__ == "__main__":
    bingx = BingX()
    bingx.get_uid_info("340238")

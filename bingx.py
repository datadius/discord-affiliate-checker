import requests
from os import getenv
import hmac
import hashlib
import time
import datetime
import orjson


class BingX:
    def __init__(self):
        self.base_url = "https://open-api.bingx.com"
        self.api_key = getenv("BINGX_API_KEY")
        self.api_secret = getenv("BINGX_API_SECRET")

    def get_uid_info(self, uid, value=99):
        endpoint = "/openApi/agent/v1/account/inviteRelationCheck"
        params = f"uid={uid}&recWindow=10000&timestamp={int(time.time() * 1000)}"
        params = self._auth(params)
        print(f"{self.base_url}{endpoint}?{params}")
        r = requests.get(
            f"{self.base_url}{endpoint}?{params}", headers={"X-BX-APIKEY": self.api_key}
        )

        user_info = orjson.loads(r.text)["data"]

        if (
            user_info.get("balanceVolume") is not None
            and user_info.get("uid") is not None
        ):
            balance = int(user_info.get("balanceVolume").partition(".")[0])
            return (
                balance > value,
                balance,
                True,
            )
        elif (
            user_info.get("uid") is not None
            and user_info.get("balanceVolume") is None
            and user_info.get("inviteResult") != False
        ):
            return False, 0, True

        return False, 0, False

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

    def get_exchange_name(self):
        return "BingX"

    def get_invited_users(self):
        endpoint = "/openApi/agent/v1/account/inviteAccountList"
        now = datetime.datetime.now()
        go_back_date = datetime.timedelta(days=6)
        start_time = now - go_back_date
        start_time = int(start_time.timestamp() * 1000)
        timestamp = int(time.time() * 1000)
        params = f"pageIndex=1&pageSize=50&timestamp={timestamp}"
        params = self._auth(params)
        print(f"{self.base_url}{endpoint}?{params}")
        r = requests.get(
            f"{self.base_url}{endpoint}?{params}", headers={"X-BX-APIKEY": self.api_key}
        )
        print(r.text)


if __name__ == "__main__":
    bingx = BingX()
    # bingx.get_invited_user
    print("True, 282, True ", bingx.get_uid_info("18137668"))
    print("False, 0, False ", bingx.get_uid_info("100"))
    print("False, 0, True ", bingx.get_uid_info("18981093"))

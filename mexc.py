import requests
from os import getenv
import hmac
import hashlib
import time
import orjson
import datetime
from urllib.parse import urlencode, quote


class MEXC:
    def __init__(self):
        self.base_url = "https://api.mexc.com"
        self.api_key = getenv("MEXC_API_KEY")
        self.api_secret = getenv("MEXC_API_SECRET")

    def get_uid_info(self, uid, value=99):
        endpoint = "/api/v3/rebate/affiliate/referral"
        timestamp = int(time.time() * 1000)
        endTime = int(time.time() * 1000)
        startTime = int(
            (datetime.datetime.now() - datetime.timedelta(days=180)).timestamp() * 1000
        )
        params = {
            "uid": uid,
            "recWindow": 10000,
            "startTime": startTime,
            "endTime": endTime,
            "timestamp": timestamp,
        }
        params["signature"] = self._auth(params)
        r = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers={"X-MEXC-APIKEY": self.api_key, "Content-Type": "application/json"},
        )

        print(r.text)
        user_info = orjson.loads(r.text)["data"]["resultList"]
        if len(user_info) > 0:
            deposit = user_info[0].get("depositAmount")
            if deposit is not None:
                deposit = int(deposit.partition(".")[0])
                uid_mexc = user_info[0].get("uid")

                if uid == uid_mexc and deposit >= value:
                    return True, deposit, True
                elif uid is not None:
                    return False, 0, True

        return False, 0, False

    def _auth(self, params):
        """
        Generates authentication signature per Phemex API specifications.
        """

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        to_sign = urlencode(params, quote_via=quote)

        def generate_hmac():
            hash = hmac.new(
                self.api_secret.encode("utf-8"),
                to_sign.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        return generate_hmac()

    def get_exchange_name(self):
        return "MEXC"


if __name__ == "__main__":
    mexc = MEXC()
    print("False, 0, False", mexc.get_uid_info("1234"))
    print("True, >100, True", mexc.get_uid_info("68502381"))

import requests
from os import getenv
import hmac
import hashlib
import time
import orjson
import datetime
from urllib.parse import urlencode, quote
import secrets


class Blofin:
    def __init__(self):
        self.base_url = "https://openapi.blofin.com"
        self.api_key = getenv("BLOFIN_API_KEY")
        self.api_secret = getenv("BLOFIN_API_SECRET")
        self.api_passphrase = getenv("BLOFIN_API_PASSPHRASE")

    def get_uid_info(self, uid, value=99):
        endpoint = "https://openapi.blofin.com"
        timestamp = str(int(time.time() * 1000))
        params = {
            "uid": uid,
        }

        r = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers={"ACCESS-KEY": self.api_key,
                     "ACCESS-SIGN":self._auth(params),
                     "ACCESS-TIMESTAMP":timestamp,
                     "ACCESS-NONCE":secrets.token_urlsafe(),
                     "ACCESS-PASSPHRASE": self.api_passphrase,
                     "Content-Type": "application/json"},
        )

        print(r.text)
        user_info = orjson.loads(r.text)["data"]
        if len(user_info) > 0:
            deposit = user_info[0].get("totalDeposit")
            if deposit is not None:
                deposit = int(deposit.partition(".")[0])
                uid_blofin = user_info[0].get("uid")

                if uid == uid_blofin and deposit >= value:
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
        return "Blofin"


if __name__ == "__main__":
    blofin = Blofin()
    print("False, 0, False", blofin.get_uid_info("1234"))
    print("True, >100, True", blofin.get_uid_info("68502381"))

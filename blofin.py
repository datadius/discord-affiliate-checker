import requests
from os import getenv
import hmac
from hashlib import sha256
import base64
import time
import orjson
import datetime
import secrets


class Blofin:
    def __init__(self):
        self.base_url = "https://openapi.blofin.com"
        self.api_key = getenv("BLOFIN_API_KEY")
        self.api_secret = getenv("BLOFIN_API_SECRET")
        self.api_passphrase = getenv("BLOFIN_API_PASSPHRASE")

    def get_uid_info(self, uid, value=99):
        endpoint = "/api/v1/affiliate/invitees"
        timestamp = str(int(time.time() * 1000))

        nonce = secrets.token_urlsafe()

        prehash_string = f"{endpoint}?uid={uid}{'GET'}{timestamp}{nonce}{''}"
        print(prehash_string)

        r = requests.get(
            f"{self.base_url}{endpoint}",
            params={
                "uid": uid,
            },
            headers={
                "ACCESS-KEY": self.api_key,
                "ACCESS-SIGN": self._auth(prehash_string),
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-NONCE": nonce,
                "ACCESS-PASSPHRASE": self.api_passphrase,
                "Content-Type": "application/json",
            },
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

    def _auth(self, prehash_string):
        """
        Generates authentication signature per Phemex API specifications.
        """

        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")

        def generate_hmac():
            return base64.b64encode(
                hmac.new(self.api_secret.encode(), prehash_string.encode(), sha256)
                .hexdigest()
                .encode()
            ).decode()

        return generate_hmac()

    def get_uids(self):
        endpoint = "/api/v1/affiliate/invitees"
        timestamp = str(int(time.time() * 1000))

        nonce = secrets.token_urlsafe()

        prehash_string = f"{endpoint}{'GET'}{timestamp}{nonce}{''}"

        r = requests.get(
            f"{self.base_url}{endpoint}",
            headers={
                "ACCESS-KEY": self.api_key,
                "ACCESS-SIGN": self._auth(prehash_string),
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-NONCE": nonce,
                "ACCESS-PASSPHRASE": self.api_passphrase,
                "Content-Type": "application/json",
            },
        )

        print(r.text)

    def get_exchange_name(self):
        return "Blofin"


if __name__ == "__main__":
    blofin = Blofin()
    blofin.get_uids()
    print("False, 0, True", blofin.get_uid_info("6413673725"))
    print("False, 0, True", blofin.get_uid_info("6341236829"))
    print("False, 0, True", blofin.get_uid_info("6289116603"))
    print("False, 0, False", blofin.get_uid_info("12345"))

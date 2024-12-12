import requests
import orjson
import os


class BYDFI:
    def __init__(self):
        self.base_url = "https://www.bydfi.com/"

    def get_uid_info(self, uid, value=99):
        endpoint = f"api/agent/v1/public/partener_users_data"
        KOLuid = os.getenv("KOLuid")
        url = f"{self.base_url}{endpoint}?partener={KOLuid}"
        print(url)
        r = requests.get(url)
        print(r.text)
        if r.status_code == 200 and r.text != "":
            user_info = orjson.loads(r.text)["data"]
            if len(user_info) != 0:
                for user in user_info:
                    if user.get("uid") == str(uid):
                        if user.get("deposit") is not None:
                            balance = int(user.get("deposit").partition(".")[0])
                            return (
                                balance > value,
                                balance,
                                True,
                            )
                        elif user.get("deposit") is None:
                            return False, 0, True

        return False, 0, False

    def get_exchange_name(self):
        return "BYDFI"


if __name__ == "__main__":
    bydfi = BYDFI()
    # bydfi.get_invited_user
    print("True, 282, True ", bydfi.get_uid_info("18137668"))
    print("False, 0, False ", bydfi.get_uid_info("100"))
    print("False, 0, True ", bydfi.get_uid_info("18981093"))

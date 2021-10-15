from typing import List
from deta import Deta
import os

# new deta project
project = Deta(os.getenv("DETA_PROJECT_KEY"))

# new deta instance
DB = project.Base("PugTrackerUserConfigs")


# add new crypto to your default
def add_crypto_def(userid: str, cryptos: List[str]) -> None:
    data = DB.get(userid)

    # new key
    if data is None:
        DB.put({"defaults": cryptos}, userid)
        return

    # update exisintg
    updates = {"defaults": DB.util.append(cryptos)}

    DB.update(updates, userid)


# remove crypto from your default
def rem_crypto_def(userid: str, remcryptos: List[str]) -> None:
    data = DB.get(userid)

    if data is None:
        return

    # remove each
    for i in remcryptos:
        data["defaults"].remove(i)

    # update new
    DB.update({"defaults": data["defaults"]}, userid)


# get defaults
def get_crypto_def(userid: str) -> List[str]:
    data = DB.get(userid)

    if data is None:
        return []

    return data["defaults"]


# set default currency convert
def set_def_cur(userid: str, cur: str) -> None:
    if cur is None:
        return

    DB.update({"currency": cur}, userid)


# get default currency convert
def get_def_cur(userid: str) -> str:
    data = DB.get(userid)

    if data is None:
        return "usd"

    try:
        return data["currency"]
    except Exception:
        return "usd"

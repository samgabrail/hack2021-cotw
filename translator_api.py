try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import requests
from pydantic import BaseModel


def getRequiredLang(country: str) -> List:
    url = f"https://translator-api-qa.taethni.com/api/languages/country/{country}"
    res = requests.get(url)
    # ic(res.json())
    languages = [lang["code"] for lang in res.json()]
    return languages


def getVillages(country: str, language: str) -> List:
    url = f"https://translator-api-qa.taethni.com/api/Keys/{country}/{language}"
    res = requests.get(url)
    res = res.json()
    return res


try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

import requests

ISO_COUNTRY_CODES = [
    "AZE",
    "BTN",
    "ETH",
    "ECU",
    "BGD",
    "ESP",
    "EGY",
    "SDN",
    "TZA",
    "IND",
    "NPL",
    "KAZ",
    "UGA",
    "PAK",
    "TGO",
    "JOR",
    "LAO",
    "KHM",
    "IDN",
    "KGZ",
    "LKA",
    "VNM",
    "THA",
]
ic(len(ISO_COUNTRY_CODES))


def getRequiredLang(country: str) -> list:
    url = f"https://translator-api-qa.taethni.com/api/languages/country/{country}"
    res = requests.get(url)
    # ic(res.json())
    languages = [lang["code"] for lang in res.json()]
    return languages


def getVillages(country, language):
    url = f"https://translator-api-qa.taethni.com/api/Keys/{country}/{language}"
    res = requests.get(url)
    res = res.json()
    return len(res)


totalVillageCount = 0
for country in ISO_COUNTRY_CODES:
    villageCount = getVillages(country, "en")
    ic(country, getRequiredLang(country), villageCount)
    totalVillageCount += villageCount
ic(totalVillageCount)

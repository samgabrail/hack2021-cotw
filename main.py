try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import requests
import overpy
import json
from pydantic import BaseModel

import gis
import osm
import translator_api


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

countryCode = "EGY" ## just for testing
# 1.1 Get the adm key from translator api
villages = translator_api.getVillages(countryCode, "en")
countryLang = translator_api.getRequiredLang(countryCode)
name = villages[12]["enValue"]
key = villages[12]["key"]
ic(key)
ic(name)
ic(countryLang)

# 1.2 Get the adm level from the key
admKeyCD = len(key.split("-")) - 1
ic(admKeyCD)
# 2. Get the boundary
baseURL = gis.getBaseGIScountryURL(countryCode)
ic(baseURL)

MaxADM = gis.getMaxADM(baseURL)
ic(MaxADM)

boundary = gis.getBoundaries(baseURL, MaxADM, admKeyCD, key)
ic(boundary)
west = boundary["bbox"][0]
south = boundary["bbox"][1]
east = boundary["bbox"][2]
north = boundary["bbox"][3]
ic(west, south, east, north)

# 3. Query OpenStreetMaps (OSM) providing the (south, west, north, east) coordinates
tags = osm.getOSMtags(south, west, north, east)
ic(tags)

# Print all the languages needed per country along with the number of villages
# totalVillageCount = 0
# for country in ISO_COUNTRY_CODES:
#     villageCount = getVillages(country, "en")
#     ic(country, getRequiredLang(country), villageCount)
#     totalVillageCount += villageCount
# ic(totalVillageCount)






try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import requests
import overpy
import json
from pydantic import BaseModel


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


def getBoundaries(country):
    url = f"https://services.arcgis.com/jpbmZUwK24tWjkHJ/ArcGIS/rest/services/{country}_1_0_0/FeatureServer/4/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token="
    res = requests.get(url)
    return res.json()


# Print all the languages needed per country along with the number of villages
# totalVillageCount = 0
# for country in ISO_COUNTRY_CODES:
#     villageCount = getVillages(country, "en")
#     ic(country, getRequiredLang(country), villageCount)
#     totalVillageCount += villageCount
# ic(totalVillageCount)


# res = getBoundaries("IND")
# ic(res)

# api = overpy.Overpass()
# # fetch all ways and nodes
# result = api.query("""
# [out:json][timeout:25];
# area[name="Andorra"]->.searchArea;
# (
#   node[place~"city|town|village|hamlet"](area.searchArea);
# );
# out body;
# >;
# out skel qt;
# """)

# ic(len(result.nodes))
# nodes = result.nodes
# ic(nodes)

villageCount = getVillages("EGY", "en")
countryLang = getRequiredLang("EGY")
name = villageCount[0]["enValue"]
name = "Giza"
ic(name)
ic(countryLang)
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["ISO3166-1"="EG"][admin_level=2];
(node["name:en"="{0}"](area);
);
out center;
"""
overpass_query = overpass_query.format(name)
ic(overpass_query)
response = requests.get(overpass_url, params={"data": overpass_query})
data = response.json()
ic(data)

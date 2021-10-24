try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import requests
import overpy
import json
from pydantic import BaseModel


def getBaseGIScountryURL(countryCode: str) -> str:
    """Get the URL for a country"""
    url = "https://services.arcgis.com/jpbmZUwK24tWjkHJ/ArcGIS/rest/services?f=pjson"
    res = requests.get(url)
    for country in res.json()["services"]:
        if countryCode+"_1_0_0" in country["name"]:
            return country["url"]
    return "Could not find URL"

def getMaxADM(baseURL: str) -> int:
    """Get the maximum layer level, for NPL its adm4 so this function will return 4"""
    url = f"{baseURL}/?f=pjson"
    res = requests.get(url)
    layers = res.json()["layers"]
    return len(layers) - 1


def getBoundaries(baseURL: str, admCD: int, admKeyCD: int, key: str):
    url = f"{baseURL}/{admCD}/query?where=adm{admKeyCD}_cd+%3D+%27{key}%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=true&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token="
    res = requests.get(url)
    return res.json()


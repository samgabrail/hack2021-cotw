try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import requests
import overpy
import json
from pydantic import BaseModel


def getOSMtags(south, west, north, east):
    overpass_url = "https://lz4.overpass-api.de/api/interpreter"
    # overpass_query = """
    # [out:json];
    # area["ISO3166-1"="EG"][admin_level=2];
    # (node["name:en"="{0}"](area);
    # );
    # out center;
    # """

    overpass_query = """
    [out:json];
    node({0}, {1}, {2}, {3})[place~"city|town|village|hamlet"];
    out center;
    """
    
    overpass_query = overpass_query.format(south, west, north, east)
    response = requests.get(overpass_url, params={"data": overpass_query})
    data = response.json()
    return data


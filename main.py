try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import json
import csv
from pydantic import BaseModel

import gis
import osm
import translator_api
import pprint
import time

start = time.time()
print("[INFO] Program started at: ", start)

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
pp = pprint.PrettyPrinter(indent=4)


def countryRun(countryCode: str, outputFileRaw: str, outputFileTranslator: str):
    villageCounter = 0
    villageHit = 0
    baseURL = gis.getBaseGIScountryURL(countryCode)
    # ic(baseURL)

    MaxADM = gis.getMaxADM(baseURL)
    # ic(MaxADM)

    # 1.1 Get the adm key from translator api
    villages = translator_api.getVillages(countryCode, "en")
    countryLang = translator_api.getRequiredLang(countryCode)
    outputList = []
    with open(outputFileRaw, "w") as csv_file_raw:
        with open(outputFileTranslator, "w") as csv_file_translator:
            fieldnames_raw = ["key", "originalName", "tags"]
            fieldnames_translator = ["key", "en", "ne"]
            writer_raw = csv.DictWriter(
                csv_file_raw, fieldnames=fieldnames_raw, delimiter=","
            )
            writer_translator = csv.DictWriter(
                csv_file_translator, fieldnames=fieldnames_translator, delimiter=","
            )
            writer_raw.writeheader()
            writer_translator.writeheader()
            for village in villages:
                villageCounter += 1
                name = village["enValue"]
                key = village["key"]

                # 1.2 Get the adm level from the key
                admKeyCD = len(key.split("-")) - 1
                # 1.3 Make sure we stick with the maxADM to avoid getting too many results from OSM because we will get a much larger boundary
                if admKeyCD == MaxADM:
                    # 2. Get the boundary
                    boundary = gis.getBoundaries(baseURL, MaxADM, admKeyCD, key)
                    west = boundary["bbox"][0]
                    south = boundary["bbox"][1]
                    east = boundary["bbox"][2]
                    north = boundary["bbox"][3]
                    # ic(west, south, east, north)

                    # 3. Query OpenStreetMaps (OSM) providing the (south, west, north, east) coordinates
                    try:
                        tags = osm.getOSMtags(south, west, north, east)
                        # ic(tags)

                        elements = tags["elements"]
                        for element in elements:
                            finalTags = element["tags"]
                            output_raw = {
                                "key": key,
                                "originalName": name,
                                "tags": finalTags,
                            }
                            try:
                                if (
                                    "name:en" in finalTags
                                    and finalTags["name:en"] == name
                                ) or (
                                    "int_name" in finalTags
                                    and name in finalTags["int_name"]
                                    or (
                                        "name" in finalTags
                                        and name in finalTags["name"]
                                    )
                                ):
                                    # We have a match between translator name and OSM
                                    output_translator = {
                                        "key": key,
                                        "en": name,
                                        "ne": finalTags["name:ne"]
                                        or finalTags["alt_name"]
                                        or "",
                                    }
                                    writer_translator.writerow(output_translator)
                                    villageHit += 1
                                    ic(
                                        villageHit,
                                        villageCounter,
                                        villageHit / villageCounter,
                                        str(villageHit / villageCounter * 100) + "%",
                                    )
                            except KeyError as error:
                                ic(error)
                                ic(finalTags)
                            # for k, v in finalTags.items():
                            #     if k:
                            #         ic(name)
                            pp.pprint(output_raw)
                            outputList.append(output_raw)
                            writer_raw.writerow(output_raw)
                    except:
                        ic("Data error")
                        ic(south, west, north, east)
                else:
                    print(
                        f"[INFO]Boundary will be very large for adm: {admKeyCD}, skipping key"
                    )
    return outputList


countryCode = "NPL"
countryRun(
    countryCode,
    "outputRaw" + countryCode + ".csv",
    "outputTranslator" + countryCode + ".csv",
)  ## just for testing


for countryCode in ISO_COUNTRY_CODES:
    countryRun(countryCode, "output" + countryCode + ".csv")

ic(f"[INFO] Finished in {time.time() - start} seconds")


# Print all the languages needed per country along with the number of villages
# totalVillageCount = 0
# for country in ISO_COUNTRY_CODES:
#     villageCount = getVillages(country, "en")
#     ic(country, getRequiredLang(country), villageCount)
#     totalVillageCount += villageCount
# ic(totalVillageCount)

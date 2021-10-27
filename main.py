try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List
import csv
from helpers import buildOutputTranslator
import gis
import osm
import translator_api
import pprint
import time
import os
from decimal import Decimal

FOURPLACES = Decimal(10) ** -4


countryCode = os.environ["countryCode"]

start = time.time()
print(
    "[INFO] Program started at: ",
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)),
)

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


def countryRun(countryCode: str, outputFileRaw: str, outputFileTranslator: str) -> dict:
    villageCount = 0
    villageHit = 0
    totalVillageCount = 0

    baseURL = gis.getBaseGIScountryURL(countryCode)
    # ic(baseURL)

    MaxADM = gis.getMaxADM(baseURL)
    # ic(MaxADM)

    # 1.1 Get the adm key from translator api
    villages = translator_api.getVillages(countryCode, "en")
    totalVillageCount = len(villages)
    print(f"[INFO] Total Village Count for {countryCode}: {totalVillageCount}")

    countryLang = translator_api.getRequiredLang(countryCode)
    ic(countryLang)
    with open(outputFileRaw, "w") as csv_file_raw:
        with open(outputFileTranslator, "w") as csv_file_translator:
            fieldnames_raw = ["key", "originalName", "tags"]
            fieldnames_translator = ["key"]
            fieldnames_translator.extend(countryLang)
            writer_raw = csv.DictWriter(
                csv_file_raw, fieldnames=fieldnames_raw, delimiter=","
            )
            writer_translator = csv.DictWriter(
                csv_file_translator, fieldnames=fieldnames_translator, delimiter=","
            )
            writer_raw.writeheader()
            writer_translator.writeheader()
            for village in villages:
                villageCount += 1
                name = village["enValue"]
                key = village["key"]
                print(
                    f"[INFO] Village number {villageCount} out of {totalVillageCount} villages in {countryCode} with key: {key} and name: {name}"
                )
                # 1.2 Get the adm level from the key
                admKeyCD = len(key.split("-")) - 1
                # 1.3 Make sure we stick with the maxADM to avoid getting too many results from OSM because we will get a much larger boundary
                if admKeyCD >= MaxADM:
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
                        ic(tags)

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
                                    output_translator = buildOutputTranslator(
                                        countryLang, key, name, finalTags
                                    )
                                    writer_translator.writerow(output_translator)
                                    # Only consider a hit if we find a match in english name and there is a native name available
                                    for lang in countryLang:
                                        if lang != "en":
                                            if output_translator[lang] != "":
                                                villageHit += 1
                                                ratio = Decimal(villageHit / villageCount).quantize(FOURPLACES)
                                                percent = str(ratio * 100) + "%"
                                                print(
                                                    f"[INFO] Current village hit is {villageHit} out of village count of {villageCount} and ratio is {ratio} and percentage hit is {percent}"
                                                )
                                                break
                            except KeyError as error:
                                ic(error)
                                ic(finalTags)

                            pp.pprint(output_raw)
                            writer_raw.writerow(output_raw)
                    except:
                        ic("Data error")
                        ic(south, west, north, east)
                else:
                    print(
                        f"[INFO]Boundary will be very large for adm key: {admKeyCD} and MaxADM: {MaxADM}, skipping key"
                    )
    stats = {"villageHit": villageHit, "totalVillageCount": totalVillageCount}
    return stats


stats = countryRun(
    countryCode,
    "outputs/outputRaw" + countryCode + ".csv",
    "outputs/outputTranslator" + countryCode + ".csv",
)  ## just for testing


# for countryCode in ISO_COUNTRY_CODES:
#     countryRun(countryCode, "output" + countryCode + ".csv")
ratio = Decimal(stats["villageHit"] / stats["totalVillageCount"]).quantize(FOURPLACES)
percent = str(ratio * 100) + "%"
print(
    f"[INFO] The final stats: village hit is {stats['villageHit']} out of a total village count of {stats['totalVillageCount']} and ratio is {ratio} and percentage hit is {percent}"
)

ic(f"[INFO] Finished in {time.time() - start} seconds")

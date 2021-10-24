from os import name
from pydantic import BaseModel
from typing import List

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

countryLang = ["en", "ne", "ar"]
key = "x"
name = "Cairo"

finalTags = {
    "ele": "1720",
    "is_in": "Nepal",
    "is_in:country": "Nepal",
    "name": "Cairo",
    # "name:ne": "Giza",
    # "name:ar": "GizaAR",
    # "alt_name": "Heliopolis",
    "place": "hamlet",
    "source:ele": "survey",
}


def buildOutputTranslator(
    countryLang: List, key: str, name: str, finalTags: dict
) -> dict:
    output_translator = {"key": key}
    for lang in countryLang:
        if lang == "en":
            output_translator.update({lang: name})
        else:
            if f"name:{lang}" in finalTags:
                output_translator.update({lang: finalTags[f"name:{lang}"]})
            elif "alt_name" in finalTags:
                output_translator.update({lang: finalTags["alt_name"]})
            else:
                output_translator.update({lang: ""})
    return output_translator


output_translator = buildOutputTranslator(countryLang, key, name, finalTags)
ic(output_translator)

# output_translator = {
#     "key": key,
#     "en": name,
#     "ne": finalTags["name:ne"] or finalTags["alt_name"] or "",
# }

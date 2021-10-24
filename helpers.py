try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from typing import List

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
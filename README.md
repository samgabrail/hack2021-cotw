# Overview

Map English names of village locations to their native names

## Running the script using Docker
Note: Output CSV files are stored in an `outputs` folder in this repo. You can map a volume on your local machine to the container folder using `-v` as shown below.

The container runs under UID 1000 and GID 1000. Adjust the host machine accordingly. Most linux machines automatically have UID and GID 1000 assigned to the first user created.

Run:

```sh
export countryCode=<countryCode>
docker run -d --name ${countryCode} -e countryCode=${countryCode} -v <absolute_path_on_host>:/app/outputs samgabrail/cotw:latest
```

Example:
```sh
export countryCode=ETH
docker run -d --name ${countryCode} -e countryCode=${countryCode} -v /home/ubuntu/cotw/outputs:/app/outputs samgabrail/cotw:latest
```

## Running the script using Python

Clone this repository. Then run:

```sh
export countryCode=<countryCode>
python main.py
```
Example:
```sh
export countryCode=BTN
python main.py
```

## Process
1. Get the adm key from translator api and calculate the adm level for each key by counting the dashes
2. Loop over a country code and get the most zoomed in adm key from GIS along with the max and min long and lat coordinates of the polygon (south, west, north, east) coordinates
3. Pass these coordinates into OSM to find the tags for the names of the village and hopefully find the native name there
4. Output 2 CSV files, one matches the format needed by the translator app and the other includes more information from the OSM tags. They are prefixed with `outputTranslator{CountryCode}` and `outputRaw{CountryCode}`, respectively
5. Upload the `outputTranslator{CountryCode}` file to the translator app manually

## Output
2 files for each country. Files are located in the `outputs` folder


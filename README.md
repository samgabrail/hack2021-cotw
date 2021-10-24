# Overview

Map English names of village locations to their native names

## Process
This my thinking process

1. Get the adm key from translator api and calculate the adm level for each key by counting the dashes
2. Loop over a country code and get the most zoomed in adm key from GIS along with the max and min long and lat coordinates of the polygon (south, west, north, east) coordinates
3. Pass these coordinates into OSM to find the tags for the names of the village and hopefully find the native name there
4. Get the adm key from GIS data and upload the names to the translator app for a village via the translator API


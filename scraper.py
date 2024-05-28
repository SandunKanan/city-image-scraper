import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json

FILE_CONTAINING_ITEMS = "JSON/bird_cats.json"
FILE_OUTPUT = "output/bird_img_urls2.json"

# Load the list of cities from the JSON file
with open(FILE_CONTAINING_ITEMS, 'r') as file:
    items = json.load(file)

# replace spaces with hyphens and convert to lowercase
processed_items = []
for item in items:
    city_lower = item.lower().replace(" ", "-")
    processed_items.append(city_lower)

# Print the processed list
# print(processed_items)

# Optionally, save the processed list to a new JSON file
# with open('processed_urban_area_list.json', 'w') as file:
#     json.dump(processed_cities, file, indent=2)

# Dictionary to store the results
results = {}

# Fetch image URLs for each city
for item, orig_item in zip(processed_items, items):
    url = f"https://unsplash.com/s/photos/{item}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all `img` tags
    img_tags = soup.find_all("img")

    # Extract the `src` attribute from each `img` tag that starts with "https://plus.unsplash.com/"
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'].startswith("https://plus.unsplash.com/")]

    # Use the second image if available, otherwise get first, otherwise use null
    if len(img_urls) > 1:
        results[orig_item] = img_urls[1]
    elif len(img_urls) > 0:
        results[orig_item] = img_urls[0]
    else:
        results[orig_item] = None

    # Print the results for debugging purposes
    # print(f"{orig_item}: {results[orig_item]}")

    # Sleep for 1 second between requests
    # time.sleep(1)

# Write the results to a JSON file
with open('FILE_OUTPUT', 'w') as file:
    json.dump(results, file, indent=2)

print(f"Results saved to {FILE_OUTPUT}.json")

import requests
import urllib.request
import argparse
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search-song", dest="search")
args = parser.parse_args()
url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={args.search}"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

soup_json = soup.findAll("script")[10]
json_test = str(soup_json)
json_output = json_test[39:-45]
query_data = json.loads(json_output)
count = 0
data = []
for item in query_data["data"]["results"]:
    tempDict = {"index":count, "song_name": item["song_name"], "artist":item["artist_name"],"url":item["tab_url"]}
    if "type" not in item:
        tempDict["type"] = item["marketing_type"]
    else:
        tempDict["type"] = item["type"]
    data.append(tempDict)
    count+=1

for result in data:
    print(result["index"], " // ", result["type"], result["song_name"], result["artist"])

selection = int(input("Select an above tab."))

song_response = requests.get(data[selection]["url"])
song_soup = BeautifulSoup(song_response.text, "html.parser")
song_json = song_soup.findAll("script")[10]
song_str = str(song_json)
song_json_output = song_str[39:-45]
song_data = json.loads(song_json_output)
print(song_data["data"]["tab_view"]["wiki_tab"]["content"])

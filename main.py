import requests
import urllib.request
import argparse
from bs4 import BeautifulSoup
import json
import subprocess
import re

def get_json_data_as_string(url):
    song_response = requests.get(url)
    song_soup = BeautifulSoup(song_response.text, "html.parser")
    song_json = song_soup.findAll("script")[10]
    song_str = str(song_json)
    song_json_output = song_str[39:-45]
    return song_json_output

def get_song_data(data):
    song_data = json.loads(data)
    data = song_data["data"]["tab_view"]["wiki_tab"]["content"]
    output_without_opening = re.sub("\[ch\]", "", data)
    output = re.sub("\[\/ch\]", "", output_without_opening)
    return output

def get_songs_list(data):
    json_data = json.loads(data)
    count = 0
    data = []
    result = json_data["data"]["results"]
    if len(result) == 0:
        print("No tabs found.")
        exit(1)

    for song in result:
        tempDict = {"index":count, "song_name": song["song_name"], "artist":song["artist_name"],"url":song["tab_url"]}
        if "type" not in song:
            if song["marketing_type"] == "TabPro" or song["marketing_type"] == "Pro":
                continue
            tempDict["type"] = song["marketing_type"]
        else:
            if song["type"] == "TabPro" or song["type"] == "Pro":
                continue
            tempDict["type"] = song["type"]
        data.append(tempDict)
        count+=1

    return data



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search-song", dest="search")
    parser.add_argument("-c", "--current-song", action="store_true")
    args = parser.parse_args()

    if args.current_song:
        song = subprocess.check_output(["playerctl", "metadata", "title"]).decode("utf-8")
    else:
        song = args.search

    return song.rstrip()


if __name__ == "__main__":
    song = get_args()
    url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={song}"
    query_data = get_songs_list(get_json_data_as_string(url))
    print(query_data)
    for result in query_data:
        print(result["index"], " // ", result["type"], result["song_name"], result["artist"])

    selection = int(input("\nSelect a tab: "))
    song_url = query_data[selection]["url"]

    song_data = get_song_data(get_json_data_as_string(song_url))
    
    print("\n", song_data)
import requests
import urllib.request
import argparse
from bs4 import BeautifulSoup
import json
import subprocess
import re

def get_json_string_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    json = soup.findAll("script")[10]
    json_str = str(json)
    json_output = json_str[39:-45]
    return json_output

def get_song_data(data):
    song_data = json.loads(data)
    data = song_data["data"]["tab_view"]["wiki_tab"]["content"]
    remove_open_ch = re.sub("\[ch\]", "", data)
    output = re.sub("\[\/ch\]", "", remove_open_ch)
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

def run_song_title(url):
    query_data = get_songs_list(get_json_string_from_url(url))
    for result in query_data:
        print(result["index"], " // ", result["type"], result["song_name"], result["artist"])

    selection = int(input("\nSelect a tab: "))
    song_url = query_data[selection]["url"]

    song_data = get_song_data(get_json_string_from_url(song_url))
    
    print("\n", song_data)

def run_artist_search(url):
    json_string = get_json_string_from_url(url)
    data = json.loads(json_string)
    result = data["data"]["results"]
    count = 0
    output = []
    for artist in result:
        tempDict = {
        "index": count,
        "artist": artist["artist_name"],
        "tab_count":artist["tabs_cnt"],
        "url":artist["artist_url"]}
        output.append(tempDict)
        count += 1

    for result in output:
        print(result["index"], " // ", result["artist"], result["tab_count"], "tabs")

    selection = int(input("\nSelect an artist: "))

    artist_page = get_json_string_from_url("https://www.ultimate-guitar.com" + output[selection]["url"])
    page_data = json.loads(artist_page)
    data_songs = []
    count = 0
    for song in page_data["data"]["other_tabs"]:
        tempDict = {
        "index":count,
        "song":song["song_name"],
        "rating":song["rating"],
        "votes":song["votes"]}

        if "version" not in song: //TODO this doesnt work
            tempDict["version"]:0
        else:
            tempDict["version"]:song["version"]

        if "type" not in song:
            if song["marketing_type"] == "TabPro" or song["marketing_type"] == "Pro":
                continue
            tempDict["type"] = song["marketing_type"]
        else:
            if song["type"] == "TabPro" or song["type"] == "Pro":
                continue
            tempDict["type"] = song["type"]
        data_songs.append(tempDict)
        count+=1

    for song in data_songs:
        print(song["index"], " // ", song["song"], song["type"], song["version"], song["rating"], song["votes"])

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--search-artist", dest="artist")
    parser.add_argument("-s", "--search-song", dest="song")
    parser.add_argument("-c", "--current-song", action="store_true")
    args = parser.parse_args()
    
    if args.current_song:
        title = subprocess.check_output(["playerctl", "metadata", "title"]).decode("utf-8").strip()
        artist = subprocess.check_output(["playerctl", "metadata", "artist"]).decode("utf-8").strip()
        url = "https://www.ultimate-guitar.com/search.php?search_type=title&value={} {}".format(title, artist)
        run_song_title(url)
    elif args.artist != None:
        url = "https://www.ultimate-guitar.com/search.php?search_type=band&value={}".format(args.artist)
        run_artist_search(url)
    else:
        url = "https://www.ultimate-guitar.com/search.php?search_type=title&value={}".format(args.song)
        run_song_title(url)

    
    
   
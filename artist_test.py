import requests
from bs4 import BeautifulSoup as bs
import main

text = main.get_json_string_from_url("https://www.ultimate-guitar.com/search.php?search_type=band&value=whitney")
print(text)
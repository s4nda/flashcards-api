import json
import requests

# TODO:
# Fetch all anime titles
# Store them in JSON file

# Store to json file:
#some_data = {"konj": "kamila"}
#f = open("./animes.json", "w")
#f.write(json.dumps(some_data, indent=2))
#f.close()

# Loading from json file
#data = json.load(open("./animes.json"))

def download_anime_data():

    response = requests.get('https://animechan.vercel.app/api/available/anime')
    if response.status_code == 200:
        anime_data = response.json()
        with open('animes.json', 'w') as f:
            json.dump(anime_data, f)


def find_anime_by_name(keyword: str) -> list[str]:
    data = json.load(open("./animes.json"))
    out = []
    for item in data:
        if keyword.lower() in item.lower():
            out.append(item)
    return out


def get_quote_for_anime(anime_name: str):
    r = requests.get(f"https://animechan.vercel.app/api/random/anime?title={anime_name}")
    quote = r.json()
    return quote


print(get_quote_for_anime("Princess Mononoke"))
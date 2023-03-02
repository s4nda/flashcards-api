from dotenv import load_dotenv

load_dotenv()

import requests
from config import Config


def get_dummy():
    payload = {
        "model": "text-davinci-003",
        "prompt": "Convert movie titles into emoji.\n\nBack to the Future: 👨👴🚗🕒 \nBatman: 🤵🦇 \nTransformers: 🚗🤖 \nStar Wars:",
        "temperature": 0.8,
        "max_tokens": 60,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": ["\n"],
    }
    r = requests.post(
        "https://api.openai.com/v1/completions",
        json=payload,
        headers={"Authorization": f"Bearer {Config.openapi_access_token}"},
    )
    r.raise_for_status()
    res = r.json()
    print(res)


get_dummy()

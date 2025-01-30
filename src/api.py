import requests
from dotenv import load_dotenv
import os

load_dotenv()


panel = os.getenv("PANEL_ADDRESS")
sub = os.getenv("SUB_ADDRESS")




url = f"https://{panel}/login"

s = requests.Session()

data = {
    "username": os.getenv("PANEL_USER"),
    "password": os.getenv("PANEL_PASS")
}
headers = {
    'Accept': 'application/json',
}


res = s.post(url=url, json=data, headers=headers, timeout=15)
import requests
from bs4 import BeautifulSoup

def parse_build(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    """
    placeholder logic until I can get the site mapping. Different
    build sites will need different mapping (I think)
    """
    return {"preferred_affixes": ["Critical Strike Damage", "Strength", "Lucky Hit Chance"]}
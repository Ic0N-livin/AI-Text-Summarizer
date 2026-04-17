import requests
from bs4 import BeautifulSoup

adress_url = "https://pl.wikipedia.org/wiki/Skarb_panagiurski"

headers = {
    'User-Agent': 'ProjektEdukacyjnyDoCV/1.0 (mateuszsroda049@gmail.com)'
}

response = requests.get(adress_url, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

paragraphs = soup.find_all('p')

clean_paragraphs = ""

for paragraph in paragraphs:
    paragraph_text = paragraph.get_text()
    clean_paragraphs += paragraph_text + " "
print(clean_paragraphs[:500])

# print(paragraphs)
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

command = f"Przeczytaj poniższy tekst i wypisz 3 najważniejsze wnioski w punktach:\n\n{clean_paragraphs}"

ai_response = client.models.generate_content(
    model='models/gemini-flash-latest',
    contents=command
)

print("\n--- PODSUMOWANIE AI ---")
print(ai_response.text)
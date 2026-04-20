import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

languages = {
    "1": "Polski (default)",
    "2": "English"
}

print("Wybierz język/Choose language:")
for language in languages:
    print(f"{language}: {languages[language]}")

language = input("\nWprowadź numer języka/Enter the language number: ")

chosen_language = languages.get(language, "1")

communicates = {
    "1": "Wpisz adres URL strony Wikipedii, z której chcesz uzyskać informacje: ",
    "2": "Enter the URL of the Wikipedia page you want to get information from: "
}

adress_url = str(input(communicates.get(language, "1")))

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

command = f"Przeczytaj poniższy tekst i wypisz 3 najważniejsze wnioski w następującym języku: {chosen_language}.\n\n{clean_paragraphs}"

ai_response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=command
)

print("\n" + ai_response.text)
import requests
import time
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

languages = {
    "1": "Polski (default)",
    "2": "English"
}

translations = {
    "1": {"communicate": "Wpisz adres URL strony, z której chcesz uzyskać informacje: ", "status_code_positive": "Połączono ze stroną internetową.", "status_code_negative": "Nie udało się połączyć ze stroną.", "status_code_blocked": "Połączenie ze storną zablokowane.", "command": "Przeczytaj poniższy tekst i wypisz 3 najważniejsze wnioski po polsku:", "failure": "Nie udało się wygenerować odpowiedzi.", "exception": "Serwer przeciążony. Próba {current} z {max}. Czekam 10 sekund..."},
    "2": {"communicate": "Enter the URL of the site you want to get information from: ", "status_code_positive": "Connected with the site.", "status_code_negative": "No connection with the site.", "status_code_blocked": "Connection with the site blocked.", "command": "Read text beneath and write down 3 most important conclusions in english:", "failure": "Couldn't generate the response.", "exception": "Server overloaded. Try {current} out of {max}. Waiting 10 seconds..."}
}

print("Wybierz język/Choose language:")
for language in languages:
    print(f"{language}: {languages[language]}")

language = input("\nWprowadź numer języka/Enter the language number: ")

chosen_language = translations.get(language, translations["1"])

adress_url = str(input(chosen_language["communicate"]))

headers = {
    'User-Agent': 'ProjektEdukacyjnyDoCV/1.0 (mateuszsroda049@gmail.com)'
}

response = requests.get(adress_url, headers=headers)

if response.status_code == 200:
    print(chosen_language["status_code_positive"])
elif response.status_code == 403:
    print(chosen_language["status_code_blocked"])
else:
    print(chosen_language["status_code_negative"])

soup = BeautifulSoup(response.text, 'html.parser')

paragraphs = soup.find_all('p')

clean_paragraphs = ""

for paragraph in paragraphs:
    paragraph_text = paragraph.get_text()
    clean_paragraphs += paragraph_text + " "

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

command = f"{chosen_language["command"]}\n\n{clean_paragraphs}"

max_tries = 3
for i in range(max_tries):
    try: 
        ai_response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=command
        )
        print("\n" + ai_response.text)
        break
    except Exception as e:
        exception = chosen_language["exception"].format(current=i+1, max=max_tries)
        print(exception)
        time.sleep(10)
else:
    print(chosen_language["failure"])
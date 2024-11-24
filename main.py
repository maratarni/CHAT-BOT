from docx import Document
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import io

import eel   
import eel
import sys


import ctypes

lib = ctypes.CDLL("./test.dll")
# Definește semnăturile funcțiilor
lib.test.argtypes = [ctypes.c_int, ctypes.c_int]
lib.test.restype = ctypes.c_int  # Returnează un C-string
lib.date.restype = ctypes.c_char_p

# Apelează funcția
result = lib.date()  # Obține data ca un C-string
print(result.decode('utf-8'))

def get_resource_path(relative_path):
    """Găsește calea către resurse în cazul executabilului PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller stochează resursele în _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initializam un server eel cu pagina web din folderul 'web'
docx_path1 = get_resource_path('raspunsuri.docx')
docx_path2 = get_resource_path('intrebari.docx')
web_folder = get_resource_path('web')
eel.init(web_folder)


#imi citeste datele din word daca poate si daca nu imi zice ca nu poate
def citeste_word(cale_fisier):
    try:
        doc = Document(cale_fisier)
        paragraf_text = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
        #print(f"Conținutul fișierului {cale_fisier}: {paragraf_text}")
        return paragraf_text
    except Exception as e:
        print(f"Eroare la citirea fișierului {cale_fisier}: {e}")
        return []


#ia fiecare paragraf corespunzator intrebarii cu fiecare rasp care se afla exact la paragraful ala si il returneaza
def creeaza_dictionar_raspunsuri(cale_intrebari, cale_raspunsuri):
    # Verifică dacă fișierele există
    if not os.path.exists(cale_intrebari) or not os.path.exists(cale_raspunsuri):
        print("Unul sau ambele fișiere nu există!")
        return {}

    # Citește întrebările și răspunsurile
    intrebari = citeste_word(docx_path2)
    raspunsuri = citeste_word(docx_path1)

    # Verifică dacă numărul de întrebări și răspunsuri este egal
    if len(intrebari) != len(raspunsuri):
        print("Numărul de întrebări nu corespunde cu numărul de răspunsuri!")
        return {}

    # Creează dicționarul
    return {intrebari[i].lower(): raspunsuri[i] for i in range(len(intrebari))}


#functia care mi permite sa pun si jumate din intrebare
def find_best_matches(user_input, intrebari, threshold=70):
    """
    Căutăm cele mai bune potriviri pentru întrebarea utilizatorului.
    returnează întrebările care au un scor mai mare decât pragul.
    """
    matches = []

    # Iterăm prin întrebările din fișier și calculăm scorul pentru fiecare
    for intrebare in intrebari:
        # Comparăm întrebarea utilizatorului cu fiecare întrebare din fișier
        scor = fuzz.token_sort_ratio(user_input, intrebare.lower())

        # Dacă scorul este suficient de mare (pragul de 70)
        if scor >= 60:
            matches.append((intrebare, scor))

    # Sortăm potrivirile după scor, în ordine descrescătoare
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches


@eel.expose
def chatbot(user_input):

    # Specificați căile către fișierele Word
    intrebari = citeste_word(docx_path2)
    raspunsuri = citeste_word(docx_path1)

    # Creează dicționarul de răspunsuri
    responses = creeaza_dictionar_raspunsuri(docx_path2, docx_path1)

    if not responses:
        print("Nu s-a putut initializa chatbot-ul!")
        return

    #print("Chatbot inițializat! Tastează 'exit' pentru a ieși.")
#aici e magia
    while True:
        # user_input = input("Tu: ").lower()

        if user_input == 'exit':
            print("La revedere!")
            break

        # Caută răspunsul în dicționar
        matching_questions = find_best_matches(user_input, intrebari)

        if matching_questions:
            # Alege întrebarea cu cel mai bun scor
            best_match_question = matching_questions[0][0]  # Prima potrivire
            index = intrebari.index(best_match_question)
            raspuns = raspunsuri[index]
        elif user_input == 'data':
            raspuns = result.decode('utf-8')
        else:
            raspuns = "Îmi pare rău, nu știu să răspund la această întrebare."

        # print("Chatbot:", raspuns)
        return raspuns

# chatbot()

eel.start('index.html', size=(1920, 1080))
# am modificat in new branch
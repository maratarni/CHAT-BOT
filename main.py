from docx import Document
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



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
    intrebari = citeste_word("C:/FACULTATE/futuo/intrebari.docx")
    raspunsuri = citeste_word("C:/FACULTATE/futuo/raspunsuri.docx")

    # Verifică dacă numărul de întrebări și răspunsuri este egal
    if len(intrebari) != len(raspunsuri):
        print("Numărul de întrebări nu corespunde cu numărul de răspunsuri!")
        return {}

    # Creează dicționarul
    return {intrebari[i].lower(): raspunsuri[i] for i in range(len(intrebari))}


#functia care mi permite sa pun si jumate din intrebare
def find_best_match(user_input, intrebari):
    # Folosește fuzzy matching pentru a găsi cea mai apropiată întrebare
    best_match = process.extractOne(user_input, intrebari, scorer=fuzz.token_sort_ratio)

    # Dacă similaritatea este suficient de mare, returnează întrebarea găsită
    print(best_match)

    print(best_match[0])
    if best_match and best_match[1] > 60:
        return best_match[0]
    return None


def chatbot():

    # Specificați căile către fișierele Word
    intrebari = citeste_word("C:/FACULTATE/futuo/intrebari.docx")
    raspunsuri = citeste_word("C:/FACULTATE/futuo/raspunsuri.docx")

    # Creează dicționarul de răspunsuri
    responses = creeaza_dictionar_raspunsuri("C:/FACULTATE/futuo/intrebari.docx", "C:/FACULTATE/futuo/raspunsuri.docx")

    if not responses:
        print("Nu s-a putut initializa chatbot-ul!")
        return

    print("Chatbot inițializat! Tastează 'exit' pentru a ieși.")
#aici e magia
    while True:
        user_input = input("Tu: ").lower()

        if user_input == 'exit':
            print("La revedere!")
            break

        # Caută răspunsul în dicționar
        matching_question = find_best_match(user_input, intrebari)

        if matching_question:
            index = intrebari.index(matching_question)
            raspuns = raspunsuri[index]
        else:
            raspuns = "Îmi pare rău, nu știu să răspund la această întrebare."

        print("Chatbot:", raspuns)

chatbot()
print("paaa")

# comentariu
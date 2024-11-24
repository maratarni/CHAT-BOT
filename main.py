from docx import Document
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import eel
import sys

import ctypes

lib = ctypes.CDLL("./test.dll")

# Definește semnăturile funcțiilor  
# Defines the functions' signatures
lib.test.argtypes = [ctypes.c_int, ctypes.c_int]
lib.test.restype = ctypes.c_int  # Returnează un C-string   Returns a C-string
lib.date.restype = ctypes.c_char_p

# Apelează funcția  
# Call the function
result = lib.date()  # Obține data ca un C-string   Obtains the date as a C-string
print(result.decode('utf-8')) 

def get_resource_path(relative_path):
    """Finds the path to resources in the case of the PyInstaller executable."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller stochează resursele în _MEIPASS  
        # PyInstaller stores the resources in _MEIPASS 
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initializam un server eel cu pagina web din folderul 'web' 
# Initialize an eel server with the web page from the 'web folder'
docx_path1 = get_resource_path('raspunsuri.docx') 
docx_path2 = get_resource_path('intrebari.docx') 
web_folder = get_resource_path('web')
eel.init(web_folder)


#imi citeste datele din word daca poate si daca nu imi zice ca nu poate
#checks if the word document can be read and extracts the data from it
def read_word(file_path):
    try:
        doc = Document(file_path)
        paragraph_text = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
        #print(f"Conținutul fișierului {cale_fisier}: {paragraf_text}")
        return paragraph_text
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


#ia fiecare paragraf corespunzator intrebarii cu fiecare rasp care se afla exact la paragraful ala si il returneaza
#links questions to answers by aligning them with the same paragraph from the 2 databases
def create_answers_dictionary(questions_path, answers_path):
    # Verifică dacă fișierele există 
    # Verifies if the files exist
    if not os.path.exists(questions_path) or not os.path.exists(answers_path):
        print("One or both files do not exist!")
        return {}

    # Citește întrebările și răspunsurile 
    # Reads the questions and answers
    questions = read_word(docx_path2)
    answers = read_word(docx_path1)

    # Verifică dacă numărul de întrebări și răspunsuri este egal
    # Verifies if the number of questions matches the number of answers
    if len(questions) != len(answers):
        print("The number of questions does not match the number of answers!")
        return {}

    # Creează dicționarul 
    # Creates the dictionary
    return {questions[i].lower(): answers[i] for i in range(len(questions))}


#functia care mi permite sa pun si jumate din intrebare 
#function that allows partial or similar questions to be matched to their correct answers
#function
def find_best_matches(user_input, questions, threshold=70):
    """
    Căutăm cele mai bune potriviri pentru întrebarea utilizatorului.
    returnează întrebările care au un scor mai mare decât pragul.
    Finds the best matches for the user's question.
    Returns the questions with a greater score than the threshold.
    """
    matches = []

    # Iterăm prin întrebările din fișier și calculăm scorul pentru fiecare 
    # We iterate through the questions in the file and calculate the score for each one
    for question in questions:
        # Comparăm întrebarea utilizatorului cu fiecare întrebare din fișier 
        # We compare the user's question with all the other questions from the database
        score = fuzz.token_sort_ratio(user_input, question.lower())

        # Dacă scorul este suficient de mare (pragul de 70) 
        # If the score is high enough (threshold is 70)
        if score >= 60:
            matches.append((question, score))

    # Sortăm potrivirile după scor, în ordine descrescătoare 
    # Sort the matches by score in decreasing order
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches


@eel.expose
def chatbot(user_input):

    # Specificați căile către fișierele Word
    # Specifiy the paths to the word documents
    questions = read_word(docx_path2)
    answers = read_word(docx_path1)

    # Creează dicționarul de răspunsuri
    # Creates the answers dictionary
    responses = create_answers_dictionary(docx_path2, docx_path1)

    if not responses:
        print("Chatbot could not be initialized!")
        return

    print("Chatbot initialized! Press 'exit' to close.")
#aici e magia
#here comes the magic:))
    while True:
        # user_input = input("Tu: ").lower()

        if user_input == 'exit':
            print("See you!")
            break

        # Caută răspunsul în dicționar
        # Search the answer in the dictionary
        matching_questions = find_best_matches(user_input, questions)

        if matching_questions:
            # Alege întrebarea cu cel mai bun scor
            # Choose  the questions with the best score
            best_match_question = matching_questions[0][0]  # Prima potrivire First match
            index = questions.index(best_match_question)
            answer = answers[index]
        elif user_input == 'data':
            answer = result.decode('utf-8')
        else:
            answer = "I'm sorry, I don't know how to answer this question."

        # print("Chatbot:", raspuns)
        return answer

# chatbot()

eel.start('index.html', size=(1920, 1080))
# am modificat in new branch


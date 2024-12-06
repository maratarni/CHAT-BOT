from docx import Document
import os
from fuzzywuzzy import fuzz
import ctypes

class Chatbot:
    def __init__(self, path_intrebari, path_raspunsuri, c_library_path):
        self.path_intrebari = path_intrebari
        self.path_raspunsuri = path_raspunsuri
        self.c_library_path = c_library_path
        self.intrebari = []
        self.raspunsuri = []
        self.responses = {}
        self.c_library = None
        self._initialize_chatbot()
        self._load_c_library()

    def _read_word_file(self, file_path):
        """
        Citește textul dintr-un fișier Word și returnează o listă de paragrafe.
        """
        try:
            doc = Document(file_path)
            return [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
        except Exception as e:
            print(f"Eroare la citirea fișierului {file_path}: {e}")
            return []

    def _create_response_dict(self):
        """
        Creează un dicționar de răspunsuri bazat pe întrebări și răspunsuri citite.
        """
        if len(self.intrebari) != len(self.raspunsuri):
            print("Numărul de întrebări nu corespunde cu numărul de răspunsuri!")
            return {}

        return {self.intrebari[i].lower(): self.raspunsuri[i] for i in range(len(self.intrebari))}

    def _initialize_chatbot(self):
        """
        Inițializează chatbot-ul prin încărcarea întrebărilor și răspunsurilor din fișiere.
        """
        if not os.path.exists(self.path_intrebari) or not os.path.exists(self.path_raspunsuri):
            print("Unul sau ambele fișiere nu există!")
            return

        self.intrebari = self._read_word_file(self.path_intrebari)
        self.raspunsuri = self._read_word_file(self.path_raspunsuri)
        self.responses = self._create_response_dict()

    def _load_c_library(self):
        """
        Încarcă biblioteca C specificată în constructor.
        """
        try:
            self.c_library = ctypes.CDLL(self.c_library_path)
        except Exception as e:
            print(f"Eroare la încărcarea bibliotecii C: {e}")
            self.c_library = None

    def call_c_function(self):
        """
        Apelează funcția `date()` din biblioteca C încărcată.
        """
        if self.c_library:
            try:
                self.c_library.date()
            except AttributeError as e:
                print(f"Funcția 'date' nu a fost găsită în biblioteca C: {e}")
        else:
            print("Biblioteca C nu este încărcată!")

    def _find_best_matches(self, user_input, threshold=70):
        """
        Găsește cele mai bune potriviri pentru întrebarea utilizatorului.
        """
        matches = []

        for intrebare in self.intrebari:
            scor = fuzz.token_sort_ratio(user_input, intrebare.lower())
            if scor >= threshold:
                matches.append((intrebare, scor))

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def get_response(self, user_input):
        """
        Oferă un răspuns pe baza inputului utilizatorului.
        """
        user_input = user_input.lower()

        if user_input == "exit":
            return "La revedere!", True

        if user_input == "what day is today?":
            self.call_c_function()
            return "Am apelat funcția C pentru a obține data de astăzi.", False

        matching_questions = self._find_best_matches(user_input)
        if matching_questions:
            best_match_question = matching_questions[0][0]
            index = self.intrebari.index(best_match_question)
            return self.raspunsuri[index], False
        else:
            return "Îmi pare rău, nu știu să răspund la această întrebare.", False

    def run(self):
        """
        Rulează interacțiunea principală cu utilizatorul.
        """
        if not self.responses:
            print("Chatbot-ul nu a fost inițializat corect!")
            return

        print("Chatbot inițializat! Tastează 'exit' pentru a ieși.")
        while True:
            user_input = input("Tu: ")
            response, should_exit = self.get_response(user_input)
            print("Chatbot:", response)
            if should_exit:
                break


# Exemplu de utilizare:
if __name__ == "__main__":
    PATH_INTREBARI = "/Users/silvanburcea/Desktop/CHATBOT/intrebari.docx"
    PATH_RASPUNSURI = "/Users/silvanburcea/Desktop/CHATBOT/raspunsuri.docx"
    C_LIBRARY_PATH = "./functions.so"  # Calea către biblioteca C

    chatbot = Chatbot(PATH_INTREBARI, PATH_RASPUNSURI, C_LIBRARY_PATH)
    chatbot.run()

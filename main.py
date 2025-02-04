import json
import os
from fuzzywuzzy import fuzz
import eel
import sys
import ctypes
from platform import system
from datetime import datetime
import openai

openai.api_key = "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"

class DateProvider:
    def __init__(self, windows_dll="./functions.dll", macos_lib="./functions.so"):
        self.lib = None
        os_type = system()
        
        if os_type == 'Windows':
            try:
                self.lib = ctypes.CDLL(windows_dll)
                self._configure()
            except OSError as e:
                print(f"Warning: Could not load DLL: {e}")
        elif os_type == 'Darwin':  # Darwin is the system name for macOS
            try:
                self.lib = ctypes.CDLL(macos_lib)
                self._configure()
            except OSError as e:
                print(f"Warning: Could not load shared library: {e}")
    
    def _configure(self):
        """Configure library function signatures for both Windows DLL and macOS shared library"""
        if self.lib:
            try:
                self.lib.date.restype = ctypes.c_char_p
                self.lib.identify_source_module.argtypes = [ctypes.c_int]
                self.lib.identify_source_module.restype = ctypes.c_char_p

            except AttributeError as e:
                print(f"Warning: Could not configure library functions: {e}")
    
    def get_date(self):
        """Get current date from library or fallback to system date"""
        if self.lib:
            try:
                result = self.lib.date()
                return result.decode('utf-8')
            except (AttributeError, Exception) as e:
                print(f"Error getting date from library: {e}")
        
        # Fallback to system date
        return datetime.now().strftime("%Y-%m-%d")

class ResourceManager:
    @staticmethod
    def get_resource_path(relative_path):
        """Find the path to resources for PyInstaller executable"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

class DocumentReader:
    @staticmethod
    def read_questions(file_path):
        """Read questions from JSON file"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return [item['text'].strip() for item in data.get('questions', [])]
        except Exception as e:
            print(f"Error reading questions file {file_path}: {e}")
            return []

    @staticmethod
    def read_answers(file_path):
        """Read answers from JSON file"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return [item['text'].strip() for item in data.get('answers', [])]
        except Exception as e:
            print(f"Error reading answers file {file_path}: {e}")
            return []

class QuestionMatcher:
    @staticmethod
    def find_best_matches(user_input, questions, threshold=75):
        """Find the best matching questions for user input"""
        matches = []
        for question in questions:
            score = fuzz.token_sort_ratio(user_input, question.lower())
            if score >= threshold:
                matches.append((question, score))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

class ChatbotDatabase:
    def __init__(self, questions_path, answers_path):
        self.questions_path = questions_path
        self.answers_path = answers_path
        self.doc_reader = DocumentReader()
        self.questions = []
        self.answers = []
        self.responses = {}
        self.load_data()

    def load_data(self):
        """Load and initialize the QA database"""
        if not os.path.exists(self.questions_path) or not os.path.exists(self.answers_path):
            print("One or both files do not exist!")
            return

        self.questions = self.doc_reader.read_questions(self.questions_path)
        self.answers = self.doc_reader.read_answers(self.answers_path)

        if len(self.questions) != len(self.answers):
            print("The number of questions does not match the number of answers!")
            return

        self.responses = {q.lower(): a for q, a in zip(self.questions, self.answers)}

class Chatbot:
    def __init__(self):
        resource_manager = ResourceManager()
        self.json_path1 = resource_manager.get_resource_path('answers.json')
        self.json_path2 = resource_manager.get_resource_path('questions.json')
        self.web_folder = resource_manager.get_resource_path('web')
        self.database = ChatbotDatabase(self.json_path2, self.json_path1)
        self.date_provider = DateProvider()
        self.matcher = QuestionMatcher()
        self.conversation_history = []  # Conversation history

    def initialize_web(self):
        """Initialize the eel web interface"""
        eel.init(self.web_folder)

    def query_openai(self, user_input):
        """Query OpenAI using conversation history"""
        try:
            # Add conversation context
            messages = [{"role": "system", "content": "You are a helpful assistant. Always respond in English."}]
            messages.extend(self.conversation_history)  # Add conversation history
            messages.append({"role": "user", "content": user_input})  # Add new message

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            reply = response['choices'][0]['message']['content']
            
            # Save answer in conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})

            return reply
        except Exception as e:
            return f"Error querying OpenAI: {e}"


    def process_input(self, user_input):
        """Process user input and return the correct answer from the database"""
        if user_input.lower() == 'exit':
            return "See you!"
        
        if user_input == 'What day is today?':
            response = self.date_provider.get_date()
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        matching_questions = self.matcher.find_best_matches(user_input, self.database.questions)

        if matching_questions:
            best_match_question = matching_questions[0][0]
            index = self.database.questions.index(best_match_question)
            response = self.database.answers[index]

            if 0 <= index <= 179 and self.date_provider.lib:
                source = self.date_provider.lib.identify_source_module(index).decode('utf-8')
                response = f"{response} (Source: {source})"

            # Salvează în istoric
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})

            return response

        # If there are no matches in the databse, qeury OpenAI
        return self.query_openai(user_input)


def main():
    chatbot = Chatbot()
    chatbot.initialize_web()
    
    # Expose the process_input method to JavaScript
    @eel.expose
    def chatbot_response(user_input):
        return chatbot.process_input(user_input)
    
    # Start the web application
    eel.start('index.html', size=(1920, 1080))

if __name__ == "__main__":
    main()

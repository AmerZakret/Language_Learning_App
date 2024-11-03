import re
import random
import pymongo                #import classes
from word import Word 
from user import User

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://amer:zencbar@cluster0.vjths0i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True, tlsAllowInvalidCertificates=True)
db = client["Learning_Language_App"]

users_collection = db["users"]
words_collection = db["words"]

class LanguageLearningApp:
    #Initialize the LanguageLearningApp object.
    def __init__(self):
        self.word_list = []
        self.current_user = None 

    #Add a word to the word list and database.
    def add_word(self, word):
        self.word_list.append(word)
        words_collection.update_one({}, {"$push": {"words": word.to_dict()}}, upsert=True)

    #Register a new user.
    def register_user(self, name, password):
        if users_collection.find_one({"name": name}):
            print("User already exists.")
            return False

        if not re.match("^[A-Za-z0-9]+$", name):
            print("Invalid username. Only letters and numbers are allowed.")
            return False

        if not re.search("[0-9]+", password):
            print("Password must include at least one number.")
            return False

        new_user = User(name, password)
        users_collection.insert_one(new_user.to_dict())
        print("User registered successfully.")
        print("\n -Log in-")
        return True

    #Log in an existing user.
    def login_user(self, name, password):
        user_data = users_collection.find_one({"name": name, "password": password})
        if user_data:
            self.current_user = User(user_data["name"], user_data["password"])
            print("Logged in successfully.")
            self.load_words()
        else:
            print("Invalid username or password. Please try again.")
            self.log_in()

    #Take log in informations from user
    def log_in(self):
        name = input("Enter your username: ")
        password = input("Enter your password: ")
        self.login_user(name, password)

    #Log out the current user.
    def logout_user(self):
        self.current_user = None
        print("Logged out successfully.")

    #Continue as a guest user.
    def continue_as_guest(self):
        self.current_user = User("Guest", "")
        print("Continuing as Guest.")

    #Load words from the database.
    def load_words(self):
        word_docs = words_collection.find_one({})
        if word_docs and "words" in word_docs:
            self.word_list = [Word(word["word"], word["meaning"]) for word in word_docs["words"]]

    #Start a vocabulary quiz.
    def vocabulary_quiz(self):
        if self.current_user.name == "Guest":
            print("Please log in first.")
            return

        print("Vocabulary Quiz")
        correct_answers = 0
        questions = random.sample(self.word_list, min(5, len(self.word_list)))
        for word in questions:
            print(f"Meaning: {word.meaning}")
            answer = input("Enter the word: ")
            if answer.lower() == word.word.lower():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct word is '{word.word}'.")
                break
        print(f"\nYou got {correct_answers} correct answer(s).")

    #Start a guess word game.
    def guess_word_game(self):
        if self.current_user.name == "Guest":
            print("Please log in first.")
            return

        print("Guess Word Game")
        correct_answers = 0
        while True:
            word_docs = words_collection.find_one({})
            if word_docs and "words" in word_docs:
                words = word_docs["words"]
                random_word = random.choice(words)
                scrambled = ''.join(random.sample(random_word['word'], len(random_word['word'])))
                print(f"Scrambled word: {scrambled}")
                guess = input("Guess the word (type 'exit' to stop): ")
                if guess.lower() == random_word['word'].lower():
                    print("Correct!")
                    correct_answers += 1
                elif guess.lower() == 'exit':
                    break
                else:
                    print(f"Wrong! The word was '{random_word['word']}'.")
                    break
        print(f"\nYou guessed {correct_answers} words correctly.")

    #Start a multiple-choice quiz.
    def display_words(self):
        if self.current_user.name == "Guest":
            print("Please log in first.")
            return
        print("Words")
        for i, word in enumerate(self.word_list, start=1):
            print(f"{i}. {word.word} - {word.meaning}")

    def multiple_choice_quiz(self):
        if self.current_user.name == "Guest":
            print("Please log in first.")
            return
        
        print("\nMultiple-Choice Quiz")
        score = 0

        while True:
            question_word = random.choice(self.word_list)
            correct_meaning = question_word.meaning

            # Choose two other random meanings
            other_words = random.sample([w for w in self.word_list if w.word != question_word.word], 2)
            meanings = [correct_meaning, other_words[0].meaning, other_words[1].meaning]
            random.shuffle(meanings)

            print(f"What is the meaning of '{question_word.word}'?")
            for idx, meaning in enumerate(meanings, 1):
                print(f"{idx}. {meaning}")

            choice = input("Choose the correct meaning (1/2/3): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                if meanings[int(choice) - 1] == correct_meaning:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong! The correct meaning is '{correct_meaning}'.")
                    break
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")

        print(f"\nYour score is: {score}")
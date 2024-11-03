import pymongo
import random
import re

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://amer:zencbar@cluster0.vjths0i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True, tlsAllowInvalidCertificates=True)
db = client["Learning_Language_App"]

users_collection = db["users"]
words_collection = db["words"]

def main_menu():
    print("\nMain Menu:")
    print("1. Register User")
    print("2. Log In")
    print("3. Continue as Guest")
    print("4. Log Out")
    print("5. Exit")

def app_menu():
    print("\nApp Menu:")
    print("1. Add Words")
    print("2. Start Vocabulary Quiz")
    print("3. Start Guess Word Game")
    print("4. See Words")
    print("5. Return to Main Menu")

def add_words(app):
    while True:
        word = input("Enter word (or type 'done' to finish): ")
        if word.lower() == 'done':
            break
        meaning = input("Enter the meaning: ")
        app.add_word(Word(word, meaning))

def register_user(app):
    while True:
        name = input("Enter your username: ")
        password = input("Enter your password: ")

        if app.register_user(name, password):
            app.log_in()  # Redirect to log in after successful registration
            break

def log_in(app):
    name = input("Enter your username: ")
    password = input("Enter your password: ")
    app.login_user(name, password)

def log_out(app):
    app.logout_user()

class Word:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

    def to_dict(self):
        return {
            "word": self.word,
            "meaning": self.meaning
        }

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "password": self.password
        }

class LanguageLearningApp:
    def __init__(self):
        self.word_list = []  # Renamed to avoid conflict
        self.current_user = None

    def add_word(self, word):
        self.word_list.append(word)
        words_collection.insert_one(word.to_dict())  # Store word in MongoDB

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
        return True

    def login_user(self, name, password):
        user_data = users_collection.find_one({"name": name, "password": password})
        if user_data:
            self.current_user = User(user_data["name"], user_data["password"])
            print("Logged in successfully.")
            self.load_words()  # Load user's words from MongoDB
        else:
            print("Invalid username or password. Please try again.")
            self.log_in()

    def log_in(self):  # Renamed to avoid conflict
        name = input("Enter your username: ")
        password = input("Enter your password: ")
        self.login_user(name, password)

    def logout_user(self):
        self.current_user = None
        print("Logged out successfully.")

    def continue_as_guest(self):
        self.current_user = User("Guest", "")
        print("Continuing as Guest.")

    def load_words(self):
        user_words = words_collection.find()
        self.word_list = [Word(word["word"], word["meaning"]) for word in user_words]

    def vocabulary_quiz(self):
        if not self.current_user:
            print("Please log in or continue as a guest first.")
            return

        print("Vocabulary Quiz")
        correct_answers = 0
        questions = random.sample(self.word_list, min(5, len(self.word_list)))
        for word in questions:
            answer = input(f"What is the meaning of '{word.word}'? ")
            if answer.lower() == word.meaning.lower():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct meaning is '{word.meaning}'.")
                break  # End quiz if the answer is wrong
        print(f"\nYou got {correct_answers} correct answer.")

    def guess_word_game(self):
        if not self.current_user:
            print("Please log in or continue as a guest first.")
            return

        print("Guess Word Game")
        correct_answers = 0
        while True:
            words_cursor = words_collection.find_one({}, {"_id": 0, "words": 1})
            words = words_cursor['words']

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
                break  # End game if the answer is wrong
        print(f"\nYou guessed {correct_answers} words correctly.")

    def display_words(self):
        print("Words")
        for i, word in enumerate(self.word_list, start=1):
            print(f"{i}. {word.word} - {word.meaning}")

app = LanguageLearningApp()

while True:
    main_menu()
    choice = input("Choose an option: ")

    if choice == '1':
        register_user(app)
    elif choice == '2':
        app.log_in()
    elif choice == '3':
        app.continue_as_guest()
    elif choice == '4':
        log_out(app)
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")

    while app.current_user:
        app_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            add_words(app)
        elif choice == '2':
            app.vocabulary_quiz()
        elif choice == '3':
            app.guess_word_game()
        elif choice == '4':
            app.display_words()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

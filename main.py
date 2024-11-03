#importing classes
from language_learning_app import LanguageLearningApp
from word import Word

#user main menu
def main_menu():
    print("\nMain Menu:")
    print("1. Register User")
    print("2. Log In")
    print("3. Continue as Guest")
    print("4. Log Out")
    print("5. Exit")

#user app menu
def app_menu():
    print("\nApp Menu:")
    print("1. Add Words")
    print("2. Start Vocabulary Quiz")
    print("3. Start Guess Word Game")
    print("4. Start Multiple-Choice Quiz")
    print("5. See Words")
    print("6. Return to Main Menu")

def add_words(app):
    print("\n -Adding words-")
    if app.current_user.name == "Guest":
            print("Please log in first.")
            return
    while True:
        word = input("Enter word (or type 'done' to finish): ")
        if word.lower() == 'done':
            break
        meaning = input("Enter the meaning: ")
        app.add_word(Word(word, meaning))

def register_user(app):
    while True:
        print("\n -Register-")
        name = input("Enter your username: ")
        password = input("Enter your password: ")
        
        if app.register_user(name, password):
            app.log_in()
            break

def log_in(app):
    print("\n -Log in-")
    app.log_in()

def log_out(app):
    print("\n -Log out-")
    app.logout_user()

app = LanguageLearningApp()

while True:
    main_menu()
    choice = input("Choose an option: ")

    if choice == '1':
        register_user(app)
    elif choice == '2':
        log_in(app)
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
            app.multiple_choice_quiz()
        elif choice == '5':
            app.display_words()
        elif choice == '6':
            break  
        else:
            print("Invalid choice. Please try again.")
            app_menu()

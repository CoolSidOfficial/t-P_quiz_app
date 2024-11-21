import getpass
import json
import os
import bcrypt
from colorama import init, Fore, Style

init(autoreset=True)

quiz_data = {
    "Science": [
        {"question": "What planet is known as the Red Planet?", "options": ["Mars", "Venus", "Jupiter", "Earth"], "answer": "Mars"},
        {"question": "What is the symbol for water?", "options": ["H2O", "O2", "CO2", "H2"], "answer": "H2O"},
        {"question": "What gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "answer": "Carbon dioxide"},
        {"question": "What is the speed of light in m/s?", "options": ["300000", "299792458", "150000000", "299792500"], "answer": "299792458"}
    ],
    "History": [
        {"question": "Who was the first President of the United States?", "options": ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"], "answer": "George Washington"},
        {"question": "In which year did World War II end?", "options": ["1945", "1940", "1939", "1950"], "answer": "1945"},
        {"question": "What wall divided Berlin from 1961 to 1989?", "options": ["Berlin Wall", "Great Wall of China", "Iron Curtain", "Atlantic Wall"], "answer": "Berlin Wall"},
        {"question": "Who discovered America?", "options": ["Christopher Columbus", "Marco Polo", "Ferdinand Magellan", "Vasco da Gama"], "answer": "Christopher Columbus"}
    ],
    "Geography": [
        {"question": "What is the capital of France?", "options": ["Paris", "Berlin", "Rome", "Madrid"], "answer": "Paris"},
        {"question": "Which continent is known as the Dark Continent?", "options": ["Africa", "Asia", "Australia", "South America"], "answer": "Africa"},
        {"question": "What is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile"},
        {"question": "What is the tallest mountain in the world?", "options": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"], "answer": "Mount Everest"}
    ],
    "Math": [
        {"question": "What is 8 * 7?", "options": ["56", "64", "49", "48"], "answer": "56"},
        {"question": "What is the square root of 64?", "options": ["8", "6", "7", "9"], "answer": "8"},
        {"question": "What is the value of Pi to 2 decimal places?", "options": ["3.14", "2.71", "1.41", "3.13"], "answer": "3.14"},
        {"question": "What is 12 squared?", "options": ["144", "121", "169", "100"], "answer": "144"}
    ]
}

users_file = "users.json"

def display_welcome():
    os.system("cls")
    print(Fore.CYAN + Style.BRIGHT)
    print(Fore.GREEN+r"""
    
  ________  __     ___      ___    _______   ___       _______         ______    ____  ____   __   ________   
 /"       )|" \   |"  \    /"  |  |   __ "\ |"  |     /"     "|       /    " \  ("  _||_ " | |" \ ("      "\  
(:   \___/ ||  |   \   \  //   |  (. |__) :)||  |    (: ______)      // ____  \ |   (  ) : | ||  | \___/   :) 
 \___  \   |:  |   /\\  \/.    |  |:  ____/ |:  |     \/    |       /  /    )  )(:  |  | . ) |:  |   /  ___/  
  __/  \\  |.  |  |: \.        |  (|  /      \  |___  // ___)_     (: (____/ //  \\ \__/ //  |.  |  //  \__   
 /" \   :) /\  |\ |.  \    /:  | /|__/ \    ( \_|:  \(:      "|     \         \  /\\ __ //\  /\  |\(:   / "\  
(_______/ (__\_|_)|___|\__/|___|(_______)    \_______)\_______)      \"____/\__\(__________)(__\_|_)\_______) 
                                                                                                              

    """)
    print("===========================================".center(150))
    print("         Welcome to the Quiz App!          ".center(150))
    print("===========================================".center(150))
   
    print(Fore.CYAN + "===========================================\n" + Style.RESET_ALL)

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            return json.load(file)
    return {}

def save_users(users_db):
    with open(users_file, "w") as file:
        json.dump(users_db, file)

def register(users_db):
    print(Fore.YELLOW + "\n--- Register ---")
    username = input(Fore.CYAN + "Enter a username: " + Style.RESET_ALL)
    if username in users_db:
        print(Fore.RED + "Username already taken. Try again.")
        return users_db
    
    password = getpass.getpass("Enter a password: ")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users_db[username] = hashed_password
    save_users(users_db)
    print(Fore.GREEN + "Registration successful! Please login to play.")
    return users_db

def login(users_db):
    print(Fore.YELLOW + "\n--- Login ---")
    username = input(Fore.CYAN + "Enter your username: " + Style.RESET_ALL)
    if username not in users_db:
        print(Fore.RED + "User not found. Please register.")
        return None
    
    password = getpass.getpass("Enter your password: ")
    stored_hashed_password = users_db[username].encode()
    if bcrypt.checkpw(password.encode(), stored_hashed_password):
        print(Fore.GREEN + "Login successful!")
        return username
    else:
        print(Fore.RED + "Incorrect password.")
        return None

def ask_questions(category):
    score = 0
    for q in quiz_data[category]:
        print(Fore.CYAN + "\n" + q["question"].center(150) + Style.RESET_ALL)
        for i, option in enumerate(q["options"], 1):
            print(f"{Fore.YELLOW}{i}. {option} {Style.RESET_ALL}".center(150))
        
        try:
            answer_index = int(input(Fore.CYAN + "Your answer (1-4): " + Style.RESET_ALL)) - 1
            if 0 <= answer_index < len(q["options"]) and q["options"][answer_index] == q["answer"]:
                print(Fore.GREEN + "Correct!")
                score += 1
            else:
                print(Fore.RED + f"Wrong. The correct answer is {q['answer']}.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 1 and 4.")
    return score

def quiz():
    print(Fore.MAGENTA + "\n--- Quiz Categories ---" + Style.RESET_ALL)
    categories = list(quiz_data.keys())
    for i, category in enumerate(categories, 1):
        print(f"{Fore.CYAN}{i}. {category}{Style.RESET_ALL}")
    
    try:
        choice = int(input(Fore.CYAN + "Choose a category by number: " + Style.RESET_ALL))
        if 1 <= choice <= len(categories):
            category = categories[choice - 1]
            print(f"\nYou chose {category} category.")
            score = ask_questions(category)
            print(Fore.MAGENTA + f"\nYour score in {category} category: {score}/{len(quiz_data[category])}")
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

def main():
    display_welcome()
    
    users_db = load_users()
    
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input(Fore.CYAN + "Choose an option: " + Style.RESET_ALL)
        
        if choice == "1":
            users_db = register(users_db)
        elif choice == "2":
            user = login(users_db)
            if user:
                quiz()
        elif choice == "3":
            print(Fore.CYAN + "Thank you for using the Quiz App!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()

import sqlite3
import getpass
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
    # More categories...
}

db_file = "quiz_app.db"

def initialize_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def display_welcome():
    print(Fore.CYAN + Style.BRIGHT)
    print(Fore.GREEN + r"""
    
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

def register():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print(Fore.YELLOW + "\n--- Register ---")
    username = input(Fore.CYAN + "Enter a username: " + Style.RESET_ALL)
    
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(Fore.RED + "Username already taken. Try again.")
        conn.close()
        return

    password = getpass.getpass("Enter a password: ")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(Fore.GREEN + "Registration successful! Please login to play.")
    except sqlite3.IntegrityError:
        print(Fore.RED + "Error registering user.")
    conn.close()

def login():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print(Fore.YELLOW + "\n--- Login ---")
    username = input(Fore.CYAN + "Enter your username: " + Style.RESET_ALL)
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        print(Fore.RED + "User not found. Please register.")
        return None
    
    stored_hashed_password = row[0].encode()
    password = getpass.getpass("Enter your password: ")

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
    initialize_db()
    display_welcome()
    
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input(Fore.CYAN + "Choose an option: " + Style.RESET_ALL)
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                quiz()
        elif choice == "3":
            print(Fore.CYAN + "Thank you for using the Quiz App!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()

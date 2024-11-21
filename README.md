# **Quiz App**

A fun and interactive Quiz Application built in Python that allows users to register, log in, and test their knowledge across various categories. The app can store user data using either **file handling** or an **SQLite database**, providing flexibility and scalability.

---

## **Features**
- **User Registration**:
  - Securely register users with hashed passwords using `bcrypt`.
- **User Login**:
  - Authenticate users with their stored credentials.
- **Quiz Gameplay**:
  - Choose from multiple categories like Science, History, Geography, and Math.
  - Score tracking for each category.
- **Storage Options**:
  - **File Handling**: User data is stored in a `JSON` file.
  - **SQLite Database**: User data is stored in an `SQLite` database for efficient querying and management.

---

## **Project Structure**
### **File Handling Version**
```plaintext
QuizApp/
├── quiz_app.py   # Main Python script for the Quiz App
├── users.json    # File to store user data

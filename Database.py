import sqlite3

class Database:
    def __init__(self, databaseName):
        self.instance = sqlite3.connect(databaseName)
        self.cursor = self.instance.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                correct_answer TEXT,
                fake_answer1 TEXT,
                fake_answer2 TEXT,
                fake_answer3 TEXT
            )
            '''
        )
        self.instance.commit()

    def addQuestion(self, question, correct_answer, fake_answer1, fake_answer2, fake_answer3):
        self.cursor.execute(
            """
            INSERT INTO questions (
                question, 
                correct_answer, 
                fake_answer1, 
                fake_answer2, 
                fake_answer3
            )
            VALUES (?, ?, ?, ?, ?)
            """, 
            (question, correct_answer, fake_answer1, fake_answer2, fake_answer3)
        )
        self.instance.commit()
        print("Question added")

    def getRandomQuestions(self, n = 3):
        self.cursor.execute(
            """
            SELECT * FROM questions
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (n,)
        )
        rows = self.cursor.fetchall()

        print(f"Got {n} rows")

        return rows

    def close(self):
        self.instance.close()
        print("Connection closed")
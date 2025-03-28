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
        
        # To dictionary
        # {
        #     "question": "Какова формула второго закона Ньютона?",
        #     "options": ["F = ma", "F = mv", "F = m/a", "F = a/m"],
        #     "answer": "F = ma"
        # }
        answer = []
        for row in rows:
            answer.append(
                {
                    "question": row[1],
                    "options": [row[2], row[3], row[4], row[5]],
                    "answer": row[2]
                }
            )

        return answer

    def close(self):
        self.instance.close()
        print("Connection closed")
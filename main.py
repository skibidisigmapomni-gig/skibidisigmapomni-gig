import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup,QAbstractButton, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


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

PATH_TO_DATABASE = "Questions"

class Quiz(QWidget):
    def __init__(self):
        super().__init__()
        self.database = Database(PATH_TO_DATABASE)
        self.layout = QVBoxLayout()
        self.n = 1

    def init(self, n):
        self.setupWindow()
        self.loadStyleSheet("style.css")
        self.init_ui()

        return True
    def collnumber(self):
        self.label_collnumber =QLabel("Введите количество задач в тесте:", self)
        self.layout.addWidget(self.label_collnumber)

        self.lineEditCollNumber = QLineEdit()
        self.layout.addWidget(self.lineEditCollNumber)

        self.buttonCollNumber = QPushButton("Подтвердить")
        self.buttonCollNumber.clicked.connect(self.okay)
        self.layout.addWidget(self.buttonCollNumber)

    def okay(self):
        if self.lineEditCollNumber.text().isdigit():
            self.n = int(self.lineEditCollNumber.text())
        else:
            self.clearLayout()
            self.collnumber()
            return
        print(f"Entered n: {self.n}")
        self.clearLayout()
        self.show_ui()

        self.loadQuestions(self.n)
        self.load_question()

    def setupWindow(self):
        self.setWindowTitle("Тест по физике")
        self.setGeometry(100, 100, 600, 400)

    def loadStyleSheet(self, path):
        with open(path) as stylesheet:
            self.setStyleSheet(stylesheet.read())
    
    def loadQuestions(self, n):
        self.questions = self.database.getRandomQuestions(n)
        self.current_question_index = 0
        self.user_answers = []

    def run(self):
        self.collnumber()

    def init_ui(self):
        # Вопрос
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        # self.layout.addWidget(self.question_label)

        # TODO Добавить сброс выбора при переходе
        # Варианты ответов
        self.radio_group = QButtonGroup()
        self.radio_buttons = []
        for i in range(4):
            radio_button = QRadioButton()
            self.radio_group.addButton(radio_button)
            self.radio_buttons.append(radio_button)
            # self.layout.addWidget(radio_button)

        # Кнопка "Далее"
        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        # self.layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
    
    def show_ui(self):
        self.layout.addWidget(self.question_label)
        
        for radio_button in self.radio_buttons:
            self.layout.addWidget(radio_button)
        
        self.layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data["question"])
            for i, option in enumerate(question_data["options"]):
                self.radio_buttons[i].setText(option)
                self.radio_buttons[i].setChecked(False)
            self.next_button.setText("Далее" if self.current_question_index < len(self.questions) - 1 else "Завершить")
        else:
            self.show_results()

    def next_question(self):
        selected_option = None
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                selected_option = radio_button.text()
                break

        if selected_option is not None:
            self.user_answers.append(selected_option)
            self.current_question_index += 1
            self.load_question()
        else:
            self.question_label.setText("Пожалуйста, выберите ответ!")

    def show_results(self):
        correct_answers = 0
        result_text = "Результаты:\n\n"
        for i, question_data in enumerate(self.questions):
            user_answer = self.user_answers[i]
            correct_answer = question_data["answer"]
            result_text += f"Вопрос {i + 1}: {question_data['question']}\n"
            result_text += f"Ваш ответ: {user_answer}\n"
            result_text += f"Правильный ответ: {correct_answer}\n"
            result_text += "\n"
            if user_answer == correct_answer:
                correct_answers += 1

        result_text += f"Вы правильно ответили на {correct_answers} из {len(self.questions)} вопросов."
        self.question_label.setText(result_text)
        self.question_label.setAlignment(Qt.AlignLeft)
        self.next_button.hide()
        for radio_button in self.radio_buttons:
            radio_button.hide()

    def clearLayout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = Quiz()

    if quiz.init(2):
        quiz.run()
        quiz.show()
    else:
        print("Что-то пошло не так :)")

    sys.exit(app.exec_())
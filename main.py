import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup,QAbstractButton
)
from PyQt5.QtCore import Qt

from questions import questions

class Quiz(QWidget):
    def __init__(self):
        super().__init__()

    def init(self):
        self.setupWindow()
        self.loadStyleSheet("style.css")
        self.loadQuestions(questions)
        self.init_ui()

        return True

    def setupWindow(self):
        self.setWindowTitle("Тест по физике")
        self.setGeometry(100, 100, 600, 400)

    def loadStyleSheet(self, path):
        with open(path) as stylesheet:
            self.setStyleSheet(stylesheet.read())
    
    def loadQuestions(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.user_answers = []

    def run(self):
        self.load_question()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Вопрос
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        # TODO Добавить сброс выбора при переходе
        # Варианты ответов
        self.radio_group = QButtonGroup()
        self.radio_buttons = []
        for i in range(4):
            radio_button = QRadioButton()
            self.radio_group.addButton(radio_button)
            self.radio_buttons.append(radio_button)
            self.layout.addWidget(radio_button)

        # Кнопка "Далее"
        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = Quiz()

    if quiz.init():
        quiz.run()
        quiz.show()
    else:
        print("Что-то пошло не так :)")

    sys.exit(app.exec_())
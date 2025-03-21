import random

from Database import Database

def getRandom(a, b, n=3):
    return random.randint(a, b), random.randint(a, b), random.randint(a, b)

if __name__ == "__main__":
    db = Database("Questions")
    while True:
        question = input("Введите условие:")
        if question.lower() == "выход":
            break

        answer = input("Введите ответ:")
        a, b = map(int, input("Введите 2 числа для генерации случайных ответов").split())
        fake_answers = getRandom(a, b)
        
        db.addQuestion(question, answer, *fake_answers)
        
        print("Задача добавлена")
    db.close()
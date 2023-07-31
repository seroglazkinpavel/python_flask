"""
Создать страницу, на которой будет форма для ввода двух
чисел и выбор операции (сложение, вычитание, умножение
или деление) и кнопка "Вычислить"
При нажатии на кнопку будет произведено вычисление
результата выбранной операции и переход на страницу с
результатом.

"""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first = float(request.form.get('firstnum'))
        second = float(request.form.get('secondnum'))
        operation = request.form.get('operation')
        res = 0
        match operation:
            case "+":
                res = first + second
            case "-":
                res = first - second
            case "/":
                res = first / second
            case "*":
                res = first * second
        return f"{first} {operation} {second} = {res}"
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
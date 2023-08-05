"""
Создать страницу, на которой будет форма для ввода имени
и возраста пользователя и кнопка "Отправить"
При нажатии на кнопку будет произведена проверка
возраста и переход на страницу с результатом или на
страницу с ошибкой в случае некорректного возраста.
"""
from glob import escape
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = escape(request.form.get('name'))
        number = int(request.form.get('num'))
        print(name, number)
        if number < 0:
            return render_template('error.html')
        else:
            return f'Ваш возраст {number}'
    return render_template('age_form.html')


if __name__ == '__main__':
    app.run()
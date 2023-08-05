"""
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат.

"""
from glob import escape
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'title': 'Главная'
    }
    if request.method == 'POST':
        num = int(request.form.get('num'))
        context = {
            'num': num,
            'result': num * num,
        }
        return redirect(url_for('hello', name=context))
    return render_template('num_form.html', **context)

@app.route('/hello/<name>')
def hello(name):
    data = eval(name)
    print(type(data))
    return render_template('hello.html', name=data)


if __name__ == '__main__':
    app.run()
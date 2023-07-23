"""
Создать страницу, на которой будет форма для ввода имени
и электронной почты
При отправке которой будет создан cookie файл с данными
пользователя
Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка "Выйти"
При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты.
"""
from flask import Flask, flash, redirect, render_template, request, url_for, make_response

app = Flask(__name__)
app.secret_key = b'a68d1862772dcbb42725c5824bf05074a206ab04e0097fcd5a3e081b96247aac'

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Проверка данных формы
        if not request.form['mail']:
            flash('Введите mail!', 'danger')
            return redirect(url_for('form'))
        if not request.form['name']:
            flash('Введите Имя!', 'danger')
            return redirect(url_for('form'))
        # Обработка данных формы
        context = {
            'title': 'Приветствие',
            'mail': request.form['mail'],
            'name': request.form['name']
        }
        response = make_response(redirect(url_for('redirect_to_index', context=context)))
        response.headers['new_head'] = 'New value'
        response.set_cookie('username', context['name'])
        response.set_cookie('usermail', context['mail'])
        return response
    return render_template('user_mail_form.html')

@app.route('/redirect/<context>', methods=['GET', 'POST'])
def redirect_to_index(context):
    if request.method == 'POST':
        response = make_response(redirect(url_for('form')))
        response.set_cookie('usermail', max_age=0)
        response.set_cookie('username', max_age=0)
        return response
    data = eval(context)
    return render_template('hello_redirect.html', data=data)

if __name__ == '__main__':
    app.run()
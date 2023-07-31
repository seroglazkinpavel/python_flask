"""
Создать страницу, на которой будет форма для ввода имени
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с flash сообщением, где будет
выведено "Привет, {имя}!".
"""
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key =b'a68d1862772dcbb42725c5824bf05074a206ab04e0097fcd5a3e081b96247aac'

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Проверка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        # Обработка данных формы
        flash(f"Привет, {request.form['name']}!", 'success')
        return redirect(url_for('form'))
    return render_template('task8_form.html')


if __name__ == '__main__':
    app.run()

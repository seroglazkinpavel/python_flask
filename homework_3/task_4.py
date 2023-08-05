"""Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
○ Имя пользователя (обязательное поле)
○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке."""
from flask import Flask, flash, redirect, render_template, request, url_for, abort
from flask_wtf.csrf import CSRFProtect, logger
from homework_3.forms_4 import RegistrationForm
from homework_3.models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = b'8a5cc5efec19de366335664fd125a6e94eb73afc4ecc2f326934e8e3d65d3355'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/register.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')


# Декоратор exempt объекта csrf для отключения защиты от CSRF-атак для формы
@app.route('/form', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return 'No CSRF protection!'


# Для создания бд и таблиц
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')

@app.errorhandler(500)
def page_not_found(e):
    logger.error(e)
    context = {
                'title': 'Ошибка сервера',
                'url': request.base_url,
            }
    return render_template('500.html', **context), 500


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if not User.query.filter(User.username == request.form['username']).all():
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f"Привет, {username}! Вы успешно зарегестрировались!", 'success')
        else:
            abort(500)
        if not User.query.filter(User.email == request.form['email']).all():
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f"Привет, {username}! Вы успешно зарегестрировались!", 'success')
        else:
            flash(f"Такой '/{email}/'  есть! Подберите другой mail!", 'danger')

        return redirect(url_for('registration'))
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
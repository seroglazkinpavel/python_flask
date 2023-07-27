"""
Создать базу данных для хранения информации о книгах в библиотеке.
База данных должна содержать две таблицы: "Книги" и "Авторы".
В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
Необходимо создать связь между таблицами "Книги" и "Авторы".
Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.

"""
import random

from flask import Flask, render_template
from homework_3.models import db, Books, Author

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/library.db'
db.init_app(app)


@app.route('/')
def index():
    #return 'Hi'
    return render_template('base.html')


# Для создания бд и таблиц
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("add-avthor")
def add_avthor():
    count = 5
    for avthor in range(1, count + 1):
        new_avthor = Author(first_name=f'first_name{avthor}',
                            last_name=f'last_name{avthor}')
        db.session.add(new_avthor)
    db.session.commit()
    print('Avthor add in DB!')


@app.cli.command("add-books")
def add_books():
    count = 5
    for book in range(1, count + 1):
        new_books = Books(title_books=f'title_books{book}',
                          number_of_instances=random.randint(10, 30),
                          author_id=random.randint(1, 5))
        db.session.add(new_books)
    db.session.commit()
    print('Books add in DB!')


@app.route('/books/')
def all_books():
    res = db.session.query(Author, Books).join(Books, Author.id == Books.author_id).all()
    context = {'res': res,
               'len_objec': len(res)
               }
    return render_template('books.html', **context)


if __name__ == '__main__':
    app.run(debug=True)

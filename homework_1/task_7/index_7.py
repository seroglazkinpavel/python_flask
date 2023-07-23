"""
Написать функцию, которая будет выводить на экран HTML
страницу с блоками новостей.
Каждый блок должен содержать заголовок новости,
краткое описание и дату публикации.
Данные о новостях должны быть переданы в шаблон через
контекст.

"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/news/')
def news():
    news = [
        {'title': 'Python',
         'description': 'Python is a scripting programming language. It is universal, so it is suitable for solving a '
                        'variety of tasks and many platforms, starting with iOS and Android and ending with server OS. '
                        'This is an interpreted language — it is not compiled, that is, it is a plain text file before '
                        'launch. You can program on almost all platforms, the language is well designed and logical.',
         'date': '2023-01-28'
         },
        {'title': 'Java',
         'description': 'Java is a programming language and computing platform that was first released by Sun '
                        'Microsystems in 1995. The technology has evolved from a modest development to a tool that '
                        'plays a serious role in the modern digital world, providing a reliable platform for a '
                        'variety of services and applications. Innovative products and digital services being '
                        'developed for the future will also be created based on Java.',
         'date': '2022-11-28'
         },
        {'title': 'CSS',
         'description': 'CSS is a formal language for decorating and describing the appearance of a document (web page)'
                        ' written using a markup language (most often HTML or XHTML).',
         'date': '2021-10-22'
        }
    ]
    return render_template('index7.html', context=news)

if __name__ == '__main__':
    app.run()
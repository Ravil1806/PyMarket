from flask import Flask, render_template
from data import db_session
from data.user import User
from data.item import Item

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html', title='Главная страница')


@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    return render_template('sign_in.html', title='Авторизация')


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    return render_template('sign_up.html', title='Регистрация')


def main():
    db_session.global_init("db//main.db")
    # user = User()
    # user.name = "Равиль"
    # user.surname = "Сулейманов"
    # user.email = "ravil1806@email.ru"
    # session = db_session.create_session()
    # session.add(user)
    # session.commit()
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()

from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required
from data import db_session
from data.item import Item
from data.user import User

app = Flask(__name__)
app.secret_key = b'\xedw:~`\xe8&\x8e\x15\xf9)\xc5X#\xac('


categories = ['Одежда/обувь/аксессуары', 'Бижутерия/украшения',
              'Косметика/парфюмерия', 'Бытовая техника для дома/кухни/',
              'Мебель/интерьер', 'Товары для кухни', 'Продукты питания',
              'Товары для ремонта/строительства', 'Аудио-/видео-электроника',
              'Игры/приставки', 'Компьютеры/ноутбуки',
              'Оргтехника/расходники', 'Планшеты/электронные книги',
              'Телефоны', 'Комплектующие для ПК', 'Периферия для ПК',
              'Сетевое оборудование', 'Фототехника', 'Для охоты/рыбалки',
              'Для спорта, отдыха', 'Билеты/купоны', 'Книги/журналы',
              'Коллекционные предметы', 'Музыкальные инструменты',
              'Животные/товары для животных']

db_session.global_init("main.db")
session = db_session.create_session()


@app.route('/')
def index():
    return render_template('base.html', title='Главная страница')


@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.hashed_password, password):
                return redirect('/')
            else:
                flash('Неверный пароль')
                return redirect('/sign_in')
        else:
            flash('Аккаунта с данной почтой не существует')
            return redirect('/sign_in')
    else:
        return render_template('sign_in.html', title='Авторизация')


@app.route('/sign_out', methods=['GET', 'POST'])
# @login_required
def signout():
    pass


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User()
        user.email = request.form['email']
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.hashed_password = generate_password_hash(request.form['password'])
        if session.query(User).filter_by(email=user.email).first():
            flash('Аккаунт с данной эл. почтой уже существует')
            return redirect('/sign_up')
        if request.form['password'] != request.form['password2']:
            flash('Пароли не совпадают')
            return redirect('/sign_up')
        else:
            session.add(user)
            session.commit()
            return redirect('/')
    return render_template('sign_up.html', title='Регистрация')


@app.route('/add_item', methods=['GET', 'POST'])
# @login_required
def additem():
    if request.method == 'POST':
        item = Item()
        item.category = request.form['category']
        item.title = request.form['title']
        item.condition = request.form['condition']
        item.description = request.form['description']
        item.price = request.form['price']
        # item.photos = request.files['photos']
        try:
            session.add(item)
            session.commit()
            return redirect('/')
        except Exception as e:
            return f'{e}'
    else:
        return render_template('add_item.html', title='Новое объявление',
                               categories=categories)


def main():
    db_session.global_init("main.db")
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()

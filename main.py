from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.item import Item
from data.user import User

app = Flask(__name__)

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
    return render_template('sign_in.html', title='Авторизация')


@app.route('/sign_up')
def signup():
    return render_template('sign_up.html', title='Регистрация')


@app.route('/sign_up', methods=['POST'])
def signup_post():
    if len(request.form['password']) > 8 and \
            request.form['password'] == request.form['password2']:

        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        hashed_password = generate_password_hash(request.form['password'])

        user = User.query.filter_by(
            email=email).first()
        if user:
            flash('Аккаунт с данной эл. почтой уже существует')
            return redirect('/sign_up')
        new_user = User(email=email, name=name, surname=surname,
                        hashed_password=hashed_password)
        try:
            session.add(new_user)
            session.commit()
            return redirect('/')
        except Exception as e:
            return f'{e}'



@app.route('/add_item')
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

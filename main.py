from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from data import db_session
from data.item import Item

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

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


@app.route('/')
def index():
    return render_template('base.html', title='Главная страница')


@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    return render_template('sign_in.html', title='Авторизация')


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    return render_template('sign_up.html', title='Регистрация')


@app.route('/add_item', methods=['GET', 'POST'])  # Доработать!!!!!!!!!!!
def additem():
    if request.method == 'POST':
        item = Item()
        item.category = request.form['category']
        item.title = request.form['title']
        item.condition = request.form['condition']
        item.description = request.form['description']
        item.price = request.form['price']
        item.photos = request.form['photos']
        try:
            session = db_session.create_session('main.db')
            session.add(item)
            session.commit()
            return redirect('/')  # Добавить сообщение об успехе
        except Exception:
            return redirect('/sign_up')  # Добавить сообщение об ошибке
    else:
        return render_template('add_item.html', title='Новое объявление',
                               categories=categories)


def main():
    db_session.global_init("main.db")
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()

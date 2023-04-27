import os
from flask import Flask, render_template, request, redirect, flash, Response
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, LoginManager, login_user, \
    logout_user, current_user
from data import db_session
from data.item import Item
from data.user import User

app = Flask(__name__)
app.secret_key = b'\xedw:~`\xe8&\x8e\x15\xf9)\xc5X#\xac('
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

categories = ['Одежда/обувь/аксессуары', 'Бижутерия/украшения',
              'Косметика/парфюмерия', 'Бытовая техника для дома/кухни',
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

login_manager = LoginManager()
login_manager.login_view = '/sign_in'
login_manager.login_message = 'Необходимо войти в свой аккаунт'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html', title='Главная страница',
                           items=session.query(Item))


@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.hashed_password, password):
                login_user(user, remember=True)
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
@login_required
def signout():
    logout_user()
    return redirect('/')


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User()
        user.email = request.form['email']
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.hashed_password = generate_password_hash \
            (request.form['password'])
        user.confirmed = False
        if session.query(User).filter_by(email=user.email).first():
            flash('Аккаунт с данной эл. почтой уже существует')
            return redirect('/sign_up')
        if request.form['password'] != request.form['password2']:
            flash('Пароли не совпадают')
            return redirect('/sign_up')
        else:
            session.add(user)
            session.commit()
            return redirect('/sign_in')
    return render_template('sign_up.html', title='Регистрация')


@app.route('/<int:item_id>')
def get_img(item_id):
    img = session.query(Item).filter_by(id=item_id).first()
    return Response(img.photos, mimetype=img.mimetype)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def additem():
    if request.method == 'POST':
        item = Item()
        item.category = request.form['category']
        item.title = request.form['title']
        item.condition = request.form['condition']
        item.description = request.form['description']
        item.price = request.form['price']
        item.user_id = current_user.id
        file = request.files['photos']
        item.photos = file.read()
        item.mimetype = file.mimetype
        try:
            session.add(item)
            session.commit()
            return redirect('/')
        except Exception as e:
            return f'{e}'
    else:
        return render_template('add_item.html', title='Новое объявление',
                               categories=categories)


@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def item(item_id):
    cur_item = session.get(Item, item_id)
    if request.method == 'POST':
        pass
    else:
        return render_template('item.html', title=f'Объявление',
                               item=cur_item)


@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def edititem(item_id):
    cur_item = session.get(Item, item_id)
    if request.method == 'POST':
        cur_item.title = request.form['title']
        cur_item.condition = request.form['condition']
        cur_item.description = request.form['description']
        cur_item.price = request.form['price']
        file = request.files['photos']
        cur_item.photos = file.read()
        cur_item.mimetype = file.mimetype
        session.commit()
        return redirect(f'/item/{cur_item.id}')
    elif request.method == 'DELETE':
        session.delete(cur_item)
        session.commit()
        return redirect('/')
    else:
        return render_template('edit_item.html',
                               title='Редактирование объявления',
                               item=cur_item)


@app.route('/delete_item/<int:item_id>', methods=['GET', 'DELETE'])
def delete_item(item_id):
    cur_item = session.get(Item, item_id)
    if current_user == cur_item.user:
        session.delete(cur_item)
        session.commit()
        return redirect('/')
    else:
        return redirect(f'/profile/{current_user.id}')


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user_prof = load_user(user_id)
    return render_template('profile.html', name=user_prof.name,
                           surname=user_prof.surname,
                           email=user_prof.email,
                           number=user_prof.phone_number,
                           date=user_prof.created_date.strftime("%d.%m.%Y"),
                           address=user_prof.address,
                           num_items=len([i for i in user_prof.items]),
                           items=user_prof.items,
                           owner=bool(current_user.id == user_id),
                           title='Личний кабинет')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def editprofile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        current_user.surname = request.form['surname']
        current_user.address = request.form['address']
        current_user.phone_number = request.form['phone_number']
        session.commit()
        return redirect('/profile')
    else:
        return render_template('edit_profile.html',
                               title='Редактирвоание профиля',
                               name=current_user.name,
                               surname=current_user.surname,
                               email=current_user.email,
                               number=current_user.phone_number,
                               address=current_user.address)


def main():
    db_session.global_init("main.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)


if __name__ == '__main__':
    main()

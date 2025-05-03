from flask import Flask, render_template, redirect
from flask_restful import Api
import datetime

from requests import get

from data.users import User
from data import db_session
from data.jobs import Jobs
from data.users_api import blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from loginform import LoginForm, JobForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/users.db')
    app.register_blueprint(blueprint)
    db_sess = db_session.create_session()
    user = User()
    user.id = 1
    user.astropass = "1"
    user.cap_id = 1
    user.cap_pass = "1"
    user.name = 'Max'
    user.city_from = 'Kursk'
    db_sess.add(user)
    db_sess.commit()

    user = User()
    user.id = 2
    user.astropass = "2"
    user.cap_id = 1
    user.cap_pass = "2"
    user.name = 'Andy Weir'
    user.city_from = 'Wellington'
    db_sess.add(user)

    user = User()
    user.id = 3
    user.astropass = "2"
    user.cap_id = 1
    user.cap_pass = "2"
    user.name = 'Mark Watny'
    user.city_from = 'Moscow'
    db_sess.add(user)
    db_sess.commit()

    app.run()


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.work = form.work.data
        job.id = form.id.data
        job.work_size = form.work_size.data
        current_user.jobs.append(job)
        db_sess.merge(current_user)  # изменяем текущего пользователя
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Adding a Job',
                           form=form)


@app.route('/users_show/<int:user_id>', methods=['GET'])
def usersshow(user_id):
    user = get(f'http://127.0.0.1:5000/api/jobs/{user_id}')
    print(user.json())
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocode = user.json()['users']['city_from']

    geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

    # Выполняем запрос.
    response = get(geocoder_request)
    yaurl = ''
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Печатаем извлечённые из ответа поля:
        print(toponym_address)
        ll = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos']
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        # Готовим запрос.

        yaurl = f"{server_address}ll={','.join(ll.split())}&z=10&apikey={api_key}"
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    print(yaurl)
    return render_template('showman.html', yaurl=yaurl, name=user.json()['users']['name'],
                           town=user.json()['users']['city_from'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', news=jobs)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()

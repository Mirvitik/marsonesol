# все пароли и id это 1
from flask import Flask, render_template, redirect
import datetime
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/users.db')
    user = User()
    user.id = 1
    user.astropass = "1"
    user.cap_id = 1
    user.cap_pass = "1"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == form.id.data).first()
        if user and user.check_password(form.password.data, form.captain_password.data):
            login_user(user, remember=True)  # ассоциирует
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
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.jobs import JobsForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    db_sess = db_session.create_session()
    data = db_sess.query(Jobs, User).filter(Jobs.team_leader == User.id)

    return render_template("index.html", title="Новости", data=data)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect("/")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template("login.html", title="Авторизация",
                               message="Неправильный логин или пароль", form=form)

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(job=form.job.data, 
                    work_size=form.work_size.data,
                    collaborators=form.collaborators.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    is_finished=form.is_finished.data,
                    team_leader=form.team_leader.data)
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости',
                           form=form)
def main():
    db_session.global_init("db/blogs.db")

    db_sess = db_session.create_session()

    # user = User(surname="Scott", name="Ridley",
    #             age=21, position="captain",
    #             speciality="research engineer",
    #             address="module_1", email="scott_chief@mars.org")
    # db_sess.add(user)
    # user = User(surname="Takaev", name="Shamil",
    #             age=25, position="engineer",
    #             speciality="engineer",
    #             address="module_2", email="shamil@earth.org")
    # db_sess.add(user)
    # user = User(surname="Takaev", name="Adam",
    #             age=27, position="specialist",
    #             speciality="speciality",
    #             address="module_1", email="adam@neptun.org")
    # db_sess.add(user)
    # job = Jobs(team_leader=1, job="deployment of residental modules 1 and 2",
    #           work_size=15, collaborators="2, 3", is_finished=False)
    # db_sess.add(job)
    # db_sess.commit()
    # u = db_sess.query(User).filter(User.name=="Shamil").first()
    # job = Jobs(team_leader=u.id, job="Exploration of mineral resources", work_size=10,
    #            collaborators="4, 3", is_finished=False)
    # db_sess.add(job)
    # db_sess.commit()

    # users = db_sess.query(User).filter(User.address == "module_1")
    # users = db_sess.query(User).filter(User.speciality.notlike("%engineer%"), User.position.notlike("%engineer%"))
    # for u in users:
    #     print(u.id)

    app.run(debug=True)


if __name__ == '__main__':
    main()

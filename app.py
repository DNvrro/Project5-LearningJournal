from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, 
                        login_required, current_user)

import forms
import models


DEBUG = True

app = Flask(__name__)
app.secret_key = 'asdlkfod87093uelentry_idjfnpa..]\a]d[adfJ)&^@&_O}:><entry_IDDG{O'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DB
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You have registered!", 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
@login_required
def index():
    """Listing of all entries"""
    entries = models.Entry.select().order_by(
        models.Entry.date.desc()).limit(5)
    return render_template('index.html', entries=entries)


@app.route('/entries/<entry_id>')
def detail(entry_id):
    '''View entry details'''
    entry = models.Entry.get(models.Entry.id**entry_id)
    return render_template('detail.html', entry=entry)
    


@app.route('/entries/new', methods=['GET', 'POST'])
@login_required
def create_entry():
    """Create new entry"""
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash("New entry added!")
        models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned=form.what_i_learned.data,
            resources_to_remember=form.resources_to_remember.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)
    


@app.route('/entries/<entry_id>/edit', methods=['GET', 'POST'])
def edit_entry(entry_id):
    """Edit an entry"""
    entry = models.Entry.get(models.Entry.id**entry_id)
    form = forms.EditEntryForm(obj=entry)
    if form.validate_on_submit():
        flash("Entry edited!")
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.what_i_learned = form.what_i_learned.data
        entry.resources_to_remember = form.resources_to_remember.data
        entry.save()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)




@app.route('/entries/<entry_id>/delete')
def delete_entry(entry_id):
    """Delete an entry"""
    entry = models.Entry.get(models.Entry.id**entry_id)
    entry.delete_instance()
    flash("Entry successfully deleted.")
    return redirect(url_for('index'))


if __name__== '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='DanielNavarro',
            email='navarro@gmail.com',
            password='password',
            admin=True
            )
    except ValueError:
        pass

    app.run(debug=DEBUG)
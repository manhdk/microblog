from app import app
from flask import render_template, flash, request, url_for, redirect
from app.login_form import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'ManhDK'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in USA'
        },
        {
            'author': {'username': 'Mike'},
            'body': 'The Avengers movie was so cool'
        }
    ]
    return render_template('index.html', user = user, title = 'Home page', posts = posts)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user: {}, remember_me: {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

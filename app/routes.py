from flask import Flask, render_template, flash, redirect 
from app import app
from app.forms import LoginForm



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/dhan')
def v():
    user = {'username': 'DHAN'}
    return render_template('dhan.html', title='Home', user=user)

# if __name__=='__main__':
#     app.run(debug = False)

@app.route('/jagan')
def j():
    user = {'username': 'Miguel'}
    return render_template('jagan.html', title='Home', user=user)


@app.route('/miguel')
def m():
    user = {'username': 'Everyone'}
    posts = [
        {
            'author': {'username': 'Pragya'},
            'body': 'Problem in the lift!'
        },
        {
            'author': {'username': 'Tarun'},
            'body': 'Thank you for reporting the issue !'
        }
    ]
    return render_template('miguel.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


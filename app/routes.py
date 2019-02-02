from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post
import uuid
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        #*** get form data and write it out to a file ***
        #post = Post(body=form.post.data, author=current_user)
        postdict = {'uniqueid': form.uniqueid.data, \
                'title': form.title.data, \
                'pubdate': str(form.pubdate.data), \
                'videourl': form.videourl.data, \
                'description': form.description.data }
        postfile = postdict['uniqueid'] + '.json'
        # write to new file
        with open(postfile, 'w') as outfile:
            json.dump(postdict, outfile)
        #do append
        with open('MSNIngest.json', mode='a+', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)
            feeds.append(postdict)
            json.dump(feeds,feedsjson)

        flash('Your post has been saved to an output file!')
        return redirect(url_for('index'))
    #posts = current_user.followed_posts().all()
    #return render_template('index.html', title='Home Page', form=form, posts=posts)
    return render_template('index.html', title='Home Page', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




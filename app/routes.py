from flask import Flask, render_template, Response, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import application, db
from app.forms import LoginForm, RegistrationForm, PostForm, BlankForm
from app.models import User, Post
from datetime import datetime, timezone
import os, uuid, json


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        # datetime.strptime(str(datetime.now(timezone.utc)), '%Y-%m-%d %H:%M:%S.ffffff%Z').replace(microsecond=0).isoformat(), \
        #curdt = datetime.utcnow().isoformat
        curdt = datetime.utcnow().isoformat()
        #*** get form data and write it out to a file ***
        postdict = {
                'videourl': form.videourl.data, \
                'uniqueid': form.videourl.data, \
                'title': form.title.data, \
                'description': form.description.data, \
                'pubdate': curdt } 
                #'uniqueid': form.uniqueid.data, \
                #'pubdate': datetime.strptime(str(form.pubdate.data), '%Y-%m-%d').isoformat(), \
                #}

        #flash(postdict)
        #*** If output file doesn't exist, create it and write to new file ***
        feeds = []
        if not os.path.isfile('MSNIngest.json'):
            feeds.append(postdict)
            with open('MSNIngest.json', mode='w', encoding='utf-8') as f:
                f.write(json.dumps(feeds, indent=2))
        else:
            #*** otherwise, open the file, read in the contents and append new data ***
            with open('MSNIngest.json', mode='r', encoding='utf-8') as feedsjson:
                feeds = json.load(feedsjson)

            feeds.append(postdict)
            with open('MSNIngest.json', mode='w', encoding='utf-8') as f:
                f.write(json.dumps(feeds, indent=2))

        flash('Your post has been saved to an output file!')
        return redirect(url_for('index'))

    return render_template('index.html', title='Home Page', form=form)

@application.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    form = BlankForm()

    if not os.path.isfile('MSNIngest.json'):
        posts = []
    else:
        with open('MSNIngest.json', mode='r', encoding='utf-8') as postsjson:
            posts = json.load(postsjson)
    
    return render_template('posts.html', title='Home Page', form=form, posts=posts, publish_message='')

@application.route('/publish/', methods=['POST'])
def publish():
    from .mrsstest import convert
    import json
    import logging
    import boto3
    from botocore.exceptions import ClientError

    convert()

    """upload to S3"""
    bucket_name = 'mrsstest-022319'
    filename = 'rss2.xml'
 
    # Create the bucket policy
    #bucket_policy = {
    #    'Version': '2012-10-17',
    #    'Statement': [{
    #        'Sid': 'AddPerm',
    #        'Effect': 'Allow',
    #        'Principal': '*',
    #        'Action': ['s3:GetObject'],
    #        'Resource': "arn:aws:s3:::%s/*" % bucket_name
    #    }]
    #}

    # Convert the policy to a JSON string
    #bucket_policy = json.dumps(bucket_policy)

    # Set the new policy on the given bucket
    #s3bucket = boto3.client('s3')
    #s3bucket.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    #s3bucket.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(filename, filename, ExtraArgs={'ACL':'public-read'})
    location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, filename)

    form = BlankForm()
    posts = []

    publish_message = url
    return render_template('posts.html', title='Home Page', form=form, posts=posts, publish_message=publish_message);

@application.route('/login', methods=['GET', 'POST'])
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

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/register', methods=['GET', 'POST'])
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




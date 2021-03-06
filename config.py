import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_BUCKET   = os.environ.get("S3_BUCKET_NAME")
    S3_KEY      = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET   = os.environ.get("S3_SECRET_ACCESS_KEY")


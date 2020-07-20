import os


basedir = os.path.abspath(__file__)

# Flask_app
SECRET_KEY = 'fweifWDSLKAK@#&IEFKSLAFdhwqh@*_sAJFLKsdja@#'

# DB field
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'business.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Reservation const
DEFAULT_RESERVATION_LENGTH = 1
import os
from datetime import time


basedir = os.path.abspath(__file__)

# Flask_app
SECRET_KEY = 'fweifWDSLKAK@#&IEFKSLAFdhwqh@*_sAJFLKsdja@#'

# DB field
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'business.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Reservation const
SPACE_OPEN_HOUR = time(9)
SPACE_CLOSE_HOUR = time(18)

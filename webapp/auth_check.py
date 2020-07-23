from flask_httpauth import HTTPBasicAuth
from werkzeug import check_password_hash

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    from webapp.config import USERS as users
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
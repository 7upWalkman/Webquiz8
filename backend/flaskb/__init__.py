"""
This is the API server for the WebQuiz Web App.
It provides an API so that the Web frontend and other potential clients
can access WebQuiz storage and services.

(c) Joao Galamba, 2022
$LICENSE(MIT)
"""

from logging import (
    INFO,
    DEBUG as LOG_DEBUG,
    info,
    basicConfig,
    warning,
    error,
)

from flask import Flask, request, session
from flask_cors import CORS

from . import db
from .utils import snake_to_camel_case

################################################################################
##
##      FLASK SERVER INIT
##
################################################################################

def create_app(test_config=None):
    """
    Factory function used to create the flask/server app. Loosely 
    based on the tutorial: 
    https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/
    See:
    https://flask.palletsprojects.com/en/2.1.x/config/#builtin-configuration-values
    """

    ############################################################################
    ##
    ##      APPLICATION INITIALIZATION
    ##
    ############################################################################

    basicConfig(level=INFO)
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    flask_env = app.config.get('ENV', 'production')

    info(f"\n\n[+] STARTED IN {flask_env.upper()} MODE\n\n")

    # https://flask.palletsprojects.com/en/2.1.x/config/
    if test_config:
        app.config.from_mapping(test_config)
        info("[+] Loaded configuration from a DICT like object!")
    else:
        config_type = flask_env.capitalize()
        app.config.from_object(f'instance.config.{config_type}')
        info(f"[+] Loaded configuration '{config_type}' from CONFIG.PY")

    USER_NOT_FOUND = 'null'
    DEBUG = app.config['DEBUG']
    basicConfig(level=int(app.config['LOG_LEVEL']))
    info(f"[+] Logging level is {app.config['LOG_LEVEL']}")
    if DEBUG:
        info(f"{app.config['TESTING']=}")
        info(f"{app.config['SESSION_COOKIE_NAME']=}")
        info(f"{app.config['DATABASE']=}")
        info(f"{app.config['DATABASE_HOST']=}")
        info(f"{app.config['DATABASE_USER']=}")

    db.init_db_connector(
        host = app.config['DATABASE_HOST'],
        database = app.config['DATABASE'],
        user = app.config['DATABASE_USER'],
        password = app.config['DATABASE_PASSWORD'],
    )
    info("[+] Initialized DB CONNECTOR")

    ############################################################################
    ##
    ##      ROUTES RELATED TO USER AND SESSION MANAGEMENT
    ##
    ############################################################################

    @app.route("/user/login", methods=['POST'])
    def login():
        login_data = request.get_json()
        username = login_data['username']
        password = login_data['password']
        if (user := db.authenticate_user(username, password, snake_to_camel_case)):
            session.clear()
            session['userid'] = user['id']
            session.permanent = True
            return user
        return USER_NOT_FOUND
    #:

    @app.route("/user/login", methods=['DELETE'])
    def logout():
        session.clear()
        return ''
    #:

    @app.route("/user/current", methods=['GET'])
    def get_current_user():
        userid = session.get('userid')
        if (user := db.get_user_info(userid, snake_to_camel_case)):
            return user
        return USER_NOT_FOUND
    #:

    @app.route("/user/current", methods=['POST'])
    def create_user():
        # userid = session.get('userid')
        user_data = request.get_json()
        print('[+] CREATING USER:', user_data)
        return USER_NOT_FOUND
    #:

    ############################################################################
    ##
    ##      ROUTES FOR TESTING AND DEBUGGING PURPOSES
    ##
    ############################################################################

    if DEBUG:
        @app.route("/_login-form", methods=['GET'])
        def _login_form():
            return '''\
        <form method="POST" action="/_login">
            <div><label>Username:</label><input type="text" name="username"></div>
            <div><label>Password:</label><input type="password" name="password"></div>
            <input type="submit" value="Submit">
        </form>
        '''
        #:

        @app.route("/_login", methods=['POST'])
        def _login_test():
            username = request.form.get('username')
            pwd = request.form.get('password')
            if username == 'alb' and pwd == 'abc':
                return '<h1>Welcome back Alberto</h1>'
            return f'<h1>Unknown user {username}</h1>'
        #:

    return app
#: CREATE_APP

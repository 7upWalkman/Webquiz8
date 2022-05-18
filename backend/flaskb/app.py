from datetime import timedelta
from flask import Flask, request, session
from flask_cors import CORS


################################################################################
##
##      FLASK SERVER INIT
##
################################################################################

app = Flask(__name__)
CORS(app, supports_credentials=True)
IN_DEBUG = app.config['DEBUG']
app.config.update(
    # https://flask.palletsprojects.com/en/2.1.x/quickstart/#sessions
    # https://flask.palletsprojects.com/en/2.0.x/security/#security-cookie
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
    SECRET_KEY='8e10d234a1f8eb6f9dd6dfc3a325a0613ad2e620e5b8844cb011470492422bee',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=not IN_DEBUG,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(seconds=60),
)

USER_NOT_FOUND = 'null'

################################################################################
##
##      ROUTES RELATED TO USER AND SESSION MANAGEMENT
##
################################################################################

@app.route("/user/login", methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data['username']
    pwd = login_data['password']
    if username == 'alb' and pwd == 'abc':
        session.clear()
        session['username'] = 'alb'
        session.permanent = True
        return {
            'username': username, 
            'emailAddr': 'alb@mail.com', 
            'name': 'Alberto Antunes'
        }
    return USER_NOT_FOUND
#:

@app.route("/user/login", methods=['DELETE'])
def logout():
    session.clear()
    return ''
#:

@app.route("/user/current", methods=['GET'])
def get_current_user():
    username = session.get('username')
    if username == 'alb':
        return {
            'username': username, 
            'emailAddr': 'alb@mail.com', 
            'name': 'Alberto Antunes'
        }
    return USER_NOT_FOUND
#:

#################################################################################
##
##      ROUTES FOR TESTING AND DEBUGGING PURPOSES
##
################################################################################

@app.route("/_login-form", methods=['GET'])
def _login_form():
    return '''\
<form method="POST" action="/login-test">
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

# @app.route("/user/login", methods=['POST'])
# def login():
#     login_info = request.get_json()
#     username = login_info['username']
#     pwd = login_info['password']
#     if username == 'alb' and pwd == 'abc':
#         return {'username': username, 'name': 'Alberto Antunes'}
#     return USER_NOT_FOUND
# #:

# @app.route("/hello/<name>")
# def hello_there(name):
#     now_txt = datetime.now().strftime("%A, %d %B, %Y at %X")

#     # Filter the name argument to letters only using regular expressions. URL arguments
#     # can contain arbitrary text, so we restrict to safe characters only.
#     clean_name = "Friend"
#     match_object = re.match("[a-zA-Z]+", name)
#     if match_object:
#         clean_name = match_object.group(0)

#     return f"<p>Hello there, {clean_name}! It's {now_txt}</p>"
# #:

# @app.route("/")
# def home():
#     return {
#         'message': 'This the WebQuizz backend. You probably want to call one of the API methods.'
#     }
# #:

# DATABASE LINKS
# https://tecadmin.net/how-to-install-mysql-server-on-ubuntu-22-04/

import os
import yaml
from easydict import EasyDict as edict
from flask import Flask, request, session, render_template, jsonify, make_response, redirect, url_for
from flask_cors import CORS

import bp_auth, postgresql_db
from mail import Mail
from message import Message

# start flask
# $env:FLASK_APP = "app.py";$env:FLASK_ENV = "development";flask run --host=0.0.0.0 --port=5000
# create and configure the app
app = Flask(__name__, instance_relative_config=True, static_folder='../static/spa', static_url_path='/')

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     print(path)
#     return 'NOT FOUND', 404

# a simple page that says hello
@app.route('/info', methods=['GET'])
def get_info():
    
    session['test_sess'] = 'test'
    # app.logger.debug(app.config)
    info = dict(request.headers) | dict(session.items())

    info['remote_addr'] = request.remote_addr
    info['remote_user'] = request.remote_user
    info['origin'] = request.origin
    info['referrer'] = request.referrer
    info['full_path'] = request.full_path
    return info

@app.route('/info2', methods=['GET'])
def get_info2():

    print('session:', session.get('test_sess'))
    info = dict(request.headers) | dict(session.items())

    info['remote_addr'] = request.remote_addr
    info['remote_user'] = request.remote_user
    info['origin'] = request.origin
    info['referrer'] = request.referrer
    info['full_path'] = request.full_path
    return info

@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')

# Redirect to resource url when refresh_token and resource_url in session.
# @app.route('/resource_index')
# def res_index():
#     if 'refresh_token' in session and 'resource_url' in session:
#         resp = make_response(redirect(session['resource_url']))  
#         resp.set_cookie('refresh_token', session['refresh_token'], 
#                 httponly = app.config['AUTH'].REFRESH_TOKEN_COOKIE_HTTPONLY, 
#                 secure = app.config['AUTH'].REFRESH_TOKEN_COOKIE_SECURE, 
#                 samesite = app.config['AUTH'].REFRESH_TOKEN_COOKIE_SAMESITE)
#         return resp
#     else:
#         return 'Bad Request', 400


def setup(app):
    
    print(app.debug)
    # app.debug is true when start the development server
    if app.debug:
        with open('configs/app_dev.yaml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        config = edict(config)
        # set cors to allow refresh token authenticate from resource page
        CORS(app, resources={
            r"/*": {"origins": "https://mytest.loto:8080"}
            }, supports_credentials=True)
    else:
        with open('configs/app.yaml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        config = edict(config)

    app.config.from_mapping(config.FLASK_APP)
    app.config['AUTH'] = config.AUTH
    app.config['RESOURCE'] = config.RESOURCE
    app.mail_server = Mail(config.EMAIL.DOMAIN, config.EMAIL.PORT, config.EMAIL.SENDER, config.EMAIL.PASSWORD)
    app.message = Message()

    # registe the blueprint
    app.register_blueprint(bp_auth.bp)
    postgresql_db.init_db(app, config.DATABASE)
    wait_username = open('configs/user_id_waitlist.txt', mode='r').readlines()
    wait_username = [line.rstrip() for line in wait_username]
    app.metadata = {'wait_username': wait_username}

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


setup(app)
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True, port=app.config['PORT'], ssl_context='adhoc', host='0.0.0.0')
    
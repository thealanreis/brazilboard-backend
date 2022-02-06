import json
import traceback
from pprint import pprint
import os
from flask_cors import CORS
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import Flask
# Cross Script Request Forgery Protection
from common.app_defaults import TOKEN_TIMEOUT_TIME
from flask_session import Session


csrf = CSRFProtect()
app = db = mail = session = None
all_routes = []

def create_app():
    """
    Description:
        Creates the flask app, intializing the config files and keys

    Returns
    -------
    void
    """
    global db
    global mail
    global app
    # global session
    app = Flask(__name__, instance_relative_config=False)
    # app.config['SQLALCHEMY_ECHO'] = True # Debug apenas
    app.config['WTF_CSRF_TIME_LIMIT'] = TOKEN_TIMEOUT_TIME
    app.config['WTF_CSRF_SSL_STRICT'] = False
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    # app.config['SESSION_COOKIE_DOMAIN'] = 'https://localhost'
    app.secret_key = '123QWEZXC'
    csrf.init_app(app)


    app.CONF = load_config_files()
    initialize_mail_settings(app)

    
    # mail = Mail(app)
    db_user = app.CONF['db_user']
    db_password = app.CONF['db_password']
    db_host = app.CONF['db_host']
    db_name = app.CONF['db_name']
    db_uri = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)
    db.create_all()
    CORS(app)
    


    #Blueprints
    from endpoint import route_guard
    app.register_blueprint(route_guard.route_guard_bp)

    # Inicializa rotas do Generic Endpoint
    from endpoint.endpoint_user import UserEndpoint
    from endpoint.endpoint_forum import ForumEndpoint
    from endpoint.endpoint_topic import TopicEndpoint
    from endpoint.endpoint_post import PostEndpoint

    try:
        with app.app_context():
            UserEndpoint.initialize_routes()
            ForumEndpoint.initialize_routes()
            TopicEndpoint.initialize_routes()
            PostEndpoint.initialize_routes()

        return app

    except Exception as e:
        print(e)


def load_config_files():
    """
    Description:
        Load the private and public rsa keys, as well as the app.config file from the same directory of the application

    Returns
    -------
    void
    """

    print('Loading intialization files')

    # BASE = os.environ['PYTHONPATH']
    # # BASE = '/home/alan/1001pets-back'
    try:
        with open('./conf/app.config.json', 'r') as f_conf:

            CONF = json.load(f_conf)

            conf_keys = ['app_name',  'db_host','db_name', 'db_user', 'db_password', 'debug_mode']

            if not CONF or not all(key in CONF for key in conf_keys):
                print(
                    'Problem validating the config files, mandatory fields in app.config:')
                print(conf_keys)
                exit(1)

            return CONF

    except OSError as e:
        pprint('FATAL: The config files and keys are not present in the root directory.')
        pprint(e)
        traceback.print_exc()
        exit(1)

    except ValueError as e:
        pprint('FATAL: could not parse app.config.json')
        pprint(e)
        exit(1)

    except Exception as e:
        pprint('Uknkown exception')
        pprint(e)
        exit(1)


def initialize_mail_settings(app):
    # app.config['MAIL_SERVER'] = app.CONF['email_host']
    # app.config['MAIL_PORT'] = app.CONF['email_port']
    # app.config['MAIL_USE_TLS'] = app.CONF['email_use_tls']
    # app.config['MAIL_USERNAME'] = app.CONF['email_user']
    # app.config['MAIL_PASSWORD'] = app.CONF['email_password']
    # app.config['MAIL_DEBUG'] = False
    pass
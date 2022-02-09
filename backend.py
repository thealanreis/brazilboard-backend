import json
import traceback
from pprint import pprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from common.app_defaults import TOKEN_TIMEOUT_TIME
from flask_session import Session
# from flask_mail import Mail

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

    # Blueprints
    from endpoint import route_guard
    app.register_blueprint(route_guard.route_guard_bp)
    from endpoint.user_endpoint import user_endpoint
    from endpoint.forum_endpoint import forum_endpoint
    from endpoint.topic_endpoint import topic_endpoint
    from endpoint.post_endpoint import post_endpoint

    try:
        with app.app_context():
            forum_endpoint.initialize_routes()
            user_endpoint.initialize_routes()
            topic_endpoint.initialize_routes()
            post_endpoint.initialize_routes()
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
    try:
        with open('./conf/app.config.json', 'r') as f_conf:

            CONF = json.load(f_conf)
            conf_keys = ['app_name',  'db_host', 'db_name', 'db_user',
                         'db_password', 'debug_mode', 'backend_prefix']

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

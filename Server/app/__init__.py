from flask import Flask


def register_extensions(flask_app):
    from app.extensions import cors, jwt, mongoengine, validator, swagger

    cors.init_app(flask_app)
    jwt.init_app(flask_app)
    mongoengine.init_app(flask_app)
    validator.init_app(flask_app)
    swagger.template = flask_app.config['SWAGGER_TEMPLATE']
    swagger.init_app(flask_app)


def register_blueprints(flask_app):
    from app.blueprints import api_v1_blueprint
    from app.views import post, user

    handle_exception_func = flask_app.handle_exception
    handle_user_exception_func = flask_app.handle_user_exception
    # register_blueprint 시 defer되었던 함수들이 호출되며, flask-restful.Api._init_app()이 호출되는데
    # 해당 메소드가 app 객체의 에러 핸들러를 오버라이딩해서, 별도로 적용한 handler의 HTTPException 관련 로직이 동작하지 않음
    # 따라서 두 함수를 임시 저장해 두고, register_blueprint 이후 함수를 재할당하도록 함

    flask_app.register_blueprint(api_v1_blueprint)

    flask_app.handle_exception = handle_exception_func
    flask_app.handle_user_exception = handle_user_exception_func


def register_hooks(flask_app: Flask):
    from mongoengine import ValidationError
    from werkzeug.exceptions import HTTPException

    from app.hooks.error import (
        http_exception_handler, mongoengine_validation_error_handler, broad_exception_error_handler
    )
    from app.hooks.request_context import after_request, before_request

    flask_app.after_request(after_request)
    flask_app.before_request(before_request)
    flask_app.register_error_handler(HTTPException, http_exception_handler)
    flask_app.register_error_handler(ValidationError, mongoengine_validation_error_handler)
    flask_app.register_error_handler(Exception, broad_exception_error_handler)


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format(', '.join([config.__name__ for config in config_cls])))

    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_blueprints(flask_app)
    register_hooks(flask_app)

    return flask_app

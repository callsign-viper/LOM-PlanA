from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_validation import Validator
from flasgger import Swagger

cors = CORS()
jwt = JWTManager()
mongoengine = MongoEngine()
validator = Validator()
swagger = Swagger()


# @jwt.user_loader_callback_loader
# def user_loader_callback(identity):
#     access_token = AccessTokenModel.objects(identity=UUID(identity)).first()
#     refresh_token = RefreshTokenModel.objects(identity=UUID(identity)).first()
#
#     if access_token:
#         return access_token.key.owner
#     elif refresh_token:
#         return refresh_token.key.owner
# -> current_user가 LocalProxy로 감싸져서, 다루기 힘듬

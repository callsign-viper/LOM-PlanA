from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.post import post

api = Api(api_v1_blueprint)

api.add_resource(post.Post, '/post')
api.add_resource(post.PostItem, '/post/<id>')

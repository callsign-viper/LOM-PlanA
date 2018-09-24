from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.user import alteration, auth, signup

api = Api(api_v1_blueprint)

api.add_resource(signup.CheckIDIsAvailable, '/check/id/<id>')
api.add_resource(signup.Signup, '/signup')

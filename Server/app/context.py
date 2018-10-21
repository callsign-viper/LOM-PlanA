from flask import current_app, g, request

from app.models.user import UserModel


class _ContextProperty:
    @property
    def secret_key(self) -> str:
        return current_app.secret_key

    @property
    def user_agent(self) -> str:
        return request.headers['user_agent']

    @property
    def remote_addr(self) -> str:
        return request.remote_addr

    @property
    def requested_user_obj(self) -> 'UserModel':
        return getattr(g, 'user', None)


context_property = _ContextProperty()

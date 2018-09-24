from flask import g, request


def before_request():
    g.user_agent = request.headers['user_agent']
    g.remote_addr = request.remote_addr


def after_request(response):
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        return response

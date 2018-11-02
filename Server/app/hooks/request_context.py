from email.utils import formatdate

from flask import abort, request


def before_request():
    # 요청 처리가 시작되기 전에 입구컷 해주는 역할
    if 'user_agent' not in request.headers:
        abort(406, 'bring user agent')


def after_request(response):
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['Date'] = formatdate(timeval=None, localtime=False, usegmt=True)
    finally:
        return response

from datetime import datetime
import json

from flask import abort, g, request


def before_request():
    if 'user_agent' not in request.headers:
        abort(406, 'bring user agent')

    g.user = None
    g.user_agent = request.headers['user_agent']
    g.remote_addr = request.remote_addr


def after_request(response):
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'

        if response.is_json:
            response_payload = response.json
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if response_payload is None:
                response.data = json.dumps({
                    'at': now_str
                })
            else:
                response_payload.update({
                    'at': now_str
                })
                # for 'upsert' dictionary item
                response.data = json.dumps(response_payload)

    finally:
        return response

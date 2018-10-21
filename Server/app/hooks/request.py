from datetime import datetime
import json

from flask import abort, request


def before_request():
    # 요청 처리가 시작되기 전에 입구컷 해주는 역할
    if 'user_agent' not in request.headers:
        abort(406, 'bring user agent')


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

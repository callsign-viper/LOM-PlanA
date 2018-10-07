from flask import jsonify


def http_exception_handler(e):
    return jsonify({
        'result': e.name,
        'hint': e.description
    }), e.code


def broad_exception_error_handler(e):
    return jsonify({
        'result': 'Internal Server Error',
        'msg': str(e),
    }), 500

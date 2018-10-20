from flask import jsonify
from werkzeug.exceptions import BadRequest


def http_exception_handler(e):
    return jsonify({
        'result': e.name,
        'hint': e.description
    }), e.code


def mongoengine_validation_error_handler(e):
    return jsonify({
        'result': BadRequest.description,
        'hint': 'Validation failed - ' + ', '.join(e.to_dict().values())
    })


def broad_exception_error_handler(e):
    return jsonify({
        'result': 'Internal Server Error',
        'msg': str(e),
    }), 500

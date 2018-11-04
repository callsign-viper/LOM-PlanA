from flask import jsonify
from werkzeug.exceptions import BadRequest, InternalServerError


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
        'result': InternalServerError.description,
        'hint': str(e),
    }), 500

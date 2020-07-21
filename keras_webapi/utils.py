import logging
from flask import jsonify

def get_request_objects(request, method=None):
    response = {'get': {}, 'post': {}} 
    # get
    try:
        response['get'] = request.args
    except Exception as e:
        logging.warn('get_request_objects_error get method GET [%s]', e)
        
    # post
    try:
        response['post'] = request.get_json(silent=True)
        if not response['post']:
            raise Exception('post not found in arguments')
    except Exception as e:
        try:
            response['post'] = request.json
        except Exception as e:
            logging.warn('get_request_objects_error get method POST [%s]', e)
        
    return response


def standard_json_response(message='ok', code=200, data='none', to_json=True,
                           success=True):
    message_json = {'message': message, 'data': data, 'code': code,
                    'success': success}
    if to_json:
        return jsonify(message_json)
    return message_json
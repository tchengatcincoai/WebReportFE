import json
import flask
import decimal
import functools
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
log = logging.getLogger(__name__)


def normalize_domain(domain):
    '''
    normalize the domain, make domain to be xxx.yyy, remove the http and www
    :param domain: String, input url
    :return: String, normalized url
    '''
    try:
        if (domain.startswith('https://')):
            domain = domain[len('https://'):]
        elif (domain.startswith('http://')):
            domain = domain[len('http://'):]

        if (domain.startswith('www.')):
            domain = domain[len('www.'):]
    except Exception as ex:
        log.exception(ex)
        return 'invalid address'
    return domain


def fetch_json_data(url):
    '''
    fetch json data from url
    :param url: String
    :return: json data
    '''
    try:
        data = requests.get(url, timeout=1).json()
    except Exception as ex:
        log.exception(ex)
        return {}
    return data


def json_handler(obj):
    ''' handles normalization of sqlalchemy models '''
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def json_response(data, status_code, headers=None):
    ''' return a http json response '''
    # TODO: change to return different error page based on status code
    response_data = {'response': data, 'query_params': flask.request.args}
    resp = flask.make_response(
        json.dumps(response_data, default=json_handler),
        status_code,
        {'Content-Type': 'application/json',
         'Access-Control-Allow-Origin': '*'})
    resp.headers.extend(headers or {})
    return resp


def requires_params(required_params):
    '''
    this decorator checks if all the required params are present in the request params
    :param required_params: list of required params
    :return:
    '''
    def params_decorator(view_function):
        @functools.wraps(view_function)
        def decorated_function(*args, **kwargs):
            request_params = set(flask.request.args.keys())
            for param in required_params:
                if param not in request_params:
                    return json_response({'message': 'Please provide params for {}'.format(', '.join(required_params))}, 400)
            return view_function(*args, **kwargs)
        return decorated_function
    return params_decorator


def all_params_are_present(required_params, request_params):
    '''
    check if all required params are present
    :param required_params: list
    :param request_params: list
    :return:
    '''
    request_params = set(request_params)
    required_params = set(required_params)
    diff = required_params - request_params
    return diff is None or len(diff) == 0
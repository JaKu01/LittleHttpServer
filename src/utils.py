import os
from string import Template

CONST_DELIMITER = b'\r\n\r\n'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '../assets')


def build_response_as_bytes(status, content_type='text/html', body_str=''):
    body_length = len(body_str.encode(encoding='utf-8'))
    response = (
        f'HTTP/1.0 {status}\r\n'
        f'Content-Type: {content_type}\r\n'
        f'Content-Length: {str(body_length)}\r\n'  # length of body in bytes
        '\r\n'  # end of headers
        f'{body_str}'
    )
    return response.encode(encoding='utf-8')


def build_not_found_response() -> (bytes, str):
    tmpl = Template(read_html_file(os.path.join(ASSETS_DIR, 'error.html')))

    not_found_status = '404 Not found'
    not_found_body = tmpl.substitute(
        title=not_found_status,
        code='404',
        message='Oops! The page you are looking for cannot be found.'
    )
    return build_response_as_bytes(status=not_found_status, body_str=not_found_body), not_found_status


def build_internal_server_error_response() -> (bytes, str):
    tmpl = Template(read_html_file(os.path.join(ASSETS_DIR, 'error.html')))

    not_found_status = '500 Internal server error'
    not_found_body = tmpl.substitute(
        title=not_found_status,
        code='500',
        message='Oops! Something went wrong on our end.'
    )
    return build_response_as_bytes(status=not_found_status, body_str=not_found_body), not_found_status


def not_found_handler(verb, path, header_dict, body) -> (bytes, str):
    return build_not_found_response()


def read_html_file(file_path):
    if file_path == './':
        file_path += '/index.html'
    with open(f'{file_path}') as f:
        return f.read()

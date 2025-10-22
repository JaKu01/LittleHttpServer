CONST_DELIMITER = b'\r\n\r\n'


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


def not_found_handler(verb, path, header_dict, body) -> (bytes, str):
    return build_response_as_bytes(status='404 Not found', body_str='<h1>404 Not found</h1>'), '404 Not found'

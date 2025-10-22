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


def build_not_found_response() -> (bytes, str):
    not_found_body = read_html_file("./assets/404.html")
    not_found_status = '404 Not found'
    return build_response_as_bytes(status=not_found_status, body_str=not_found_body), not_found_status


def not_found_handler(verb, path, header_dict, body) -> (bytes, str):
    return build_not_found_response()


def read_html_file(file_path):
    if file_path == './':
        file_path += '/index.html'
    with open(f'{file_path}') as f:
        return f.read()

from handler import Handler
from handler_utils import build_response_as_bytes


def read_html_file(file_path):
    if file_path == '/':
        file_path = 'index.html'
    with open(f'.{file_path}') as f:
        return f.read()


class FileHandler(Handler):
    def handle_connection(self, verb, path, header_dict, body) -> (bytes, str):
        status = '200 OK'

        try:
            body = read_html_file(path)
        except FileNotFoundError:
            status = '404 Not Found'
            body = ''
        except Exception as e:
            status = '500 Internal Server Error'
            body = ''
            print('Unhandled exception occurred: ', e)

        return build_response_as_bytes(status=status, content_type='text/html', body_str=body), status


from handler import Handler
from utils import build_response_as_bytes, read_html_file, build_not_found_response


class FileHandler(Handler):
    def handle_connection(self, verb, path, header_dict, body) -> (bytes, str):
        status = '200 OK'

        try:
            body = read_html_file(f'./{path}')
        except (FileNotFoundError, IsADirectoryError):
            return build_not_found_response()
        except Exception as e:
            status = '500 Internal Server Error'
            body = ''
            print('Unhandled exception occurred: ', e)

        return build_response_as_bytes(status=status, content_type='text/html', body_str=body), status


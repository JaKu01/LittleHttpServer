import json

from handler import Handler
from utils import build_response_as_bytes


class JsonHandler(Handler):
    def handle_connection(self, verb, path, header_dict, body) -> (bytes, str):
        status = '200 OK'

        example_response_dict = {
            'hello': 'world',
            'production_ready': False
        }

        body = json.dumps(example_response_dict)

        return build_response_as_bytes(status=status, content_type='application/json', body_str=body), status

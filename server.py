import socket
import threading
import time
from typing import Callable, Tuple

from colorama import Fore, init

from handler import Handler
from handler_utils import not_found_handler

init(autoreset=True)

CONST_DELIMITER = b'\r\n\r\n'


def read_request(connection):
    recv_buffer = b''

    while True:
        received_data_chunk = connection.recv(1024)
        if not received_data_chunk:
            break

        recv_buffer += received_data_chunk
        if CONST_DELIMITER in recv_buffer:
            delim_index = recv_buffer.index(CONST_DELIMITER)
            return recv_buffer[:delim_index], recv_buffer[delim_index + len(CONST_DELIMITER):]


def parse_headers(header_bytes) -> (str, str, str, dict):
    headers_str = header_bytes.decode(encoding='utf-8')
    header_lines = headers_str.split('\r\n')

    first_line_parts = header_lines[0].split(' ')
    verb = first_line_parts[0]
    path = first_line_parts[1]
    version = first_line_parts[2]

    header_dict = {}
    for header in header_lines[1:]:
        header_parts = header.split(':')
        header_dict[header_parts[0].strip()] = ''.join(header_parts[1:])

    return verb, path, version, header_dict


def pretty_print_log(verb, path, status, duration_ms):
    status_color = Fore.GREEN
    if not status.startswith('2'):
        status_color = Fore.RED

    print(
        f'{Fore.CYAN}{verb} {path}{Fore.RESET} finished with status {status_color}{status}{Fore.RESET} after {Fore.CYAN}{duration_ms:.2f}{Fore.RESET} ms')


def build_path(path_parts, length):
    if length == 0:
        return '/'

    path = ''
    for idx in range(length):
        path += '/' + path_parts[idx]

    print('full path is ', path)
    return path


class HttpServer:

    def __init__(self, port=8080, ip='0.0.0.0'):
        self.handlers = {}
        self.port = port
        self.ip = ip

    def get_handler(self, verb, path):
        path_parts = [part for part in path.split('/') if part]
        num_of_parts = len(path_parts)

        for i in range(num_of_parts, -1, -1):
            full_path = build_path(path_parts, i)
            if (verb, full_path) in self.handlers:
                return self.handlers[(verb, full_path)]
        return not_found_handler

    def handle_request(self, connection):
        start = time.perf_counter()
        headers, body = read_request(connection)
        verb, path, version, header_dict = parse_headers(headers)

        request_handler = self.get_handler(verb, path)
        response = request_handler(verb, path, header_dict, body)

        connection.sendall(response[0])
        end = time.perf_counter()
        duration_ms = (end - start) * 1000
        pretty_print_log(verb, path, response[1], duration_ms)

    def add_handler(self, verb: str, path: str, handler: Handler):
        handler_key = (verb, path)
        self.handlers[handler_key] = handler.handle_connection

    def add_handle_func(self, verb, path, handle_func: Callable[[str, str, str, str], Tuple[bytes, str]]):
        handler_key = (verb, path)
        self.handlers[handler_key] = handle_func

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen()

        print(f'Starting server at port {self.port}.')

        while True:
            conn, _ = sock.accept()
            connection_thread = threading.Thread(target=self.handle_request, args=(conn,))
            connection_thread.start()

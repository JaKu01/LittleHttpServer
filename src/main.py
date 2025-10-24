from filehandler import FileHandler
from json_handler import JsonHandler
from server import HttpServer


def main():
    file_handler = FileHandler()
    json_handler = JsonHandler()

    server = HttpServer()
    server.add_handler('GET', '/', file_handler)
    server.add_handler('GET', '/json', json_handler)

    server.run()


if __name__ == '__main__':
    main()

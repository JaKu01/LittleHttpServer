from filehandler import FileHandler
from server import HttpServer


def main():
    file_handler = FileHandler()

    server = HttpServer()
    server.add_handler('GET', '/', file_handler)

    server.run()


if __name__ == '__main__':
    main()

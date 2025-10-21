from abc import abstractmethod


class Handler:

    @abstractmethod
    def handle_connection(self, verb, path, header_dict, body) -> (bytes, str):
        pass


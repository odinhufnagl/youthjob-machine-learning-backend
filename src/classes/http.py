class HttpError():
    def __init__(self, message, code):
        self.message = message
        self.code = code


class HTTPSuccess():
    def __init__(self, message, code) -> None:
        self.message = message
        self.code = code

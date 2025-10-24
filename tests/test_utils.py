import os

from src.utils import build_response_as_bytes, build_not_found_response, build_internal_server_error_response


def test_build_response_as_bytes():
    status = '200 OK'
    content_type = 'text/html'
    body_str = '<html><body><h1>Hello, World!</h1></body></html>'

    response_bytes = build_response_as_bytes(status, content_type, body_str)
    response_str = response_bytes.decode('utf-8')

    assert response_str.startswith(f'HTTP/1.0 {status}\r\n')
    assert f'Content-Type: {content_type}\r\n' in response_str
    assert f'Content-Length: {len(body_str.encode("utf-8"))}\r\n' in response_str
    assert response_str.endswith(body_str)


def test_build_not_found_response():
    res, status = build_not_found_response()

    response_str = res.decode('utf-8')
    assert "<title>404 Not found</title>" in response_str
    assert "<h1>404</h1>" in response_str
    assert "<p>Oops! The page you are looking for cannot be found.</p>" in response_str

    assert status == '404 Not found'


def test_build_internal_server_error_response():
    res, status = build_internal_server_error_response()

    response_str = res.decode('utf-8')
    assert "<title>500 Internal server error</title>" in response_str
    assert "<h1>500</h1>" in response_str
    assert "<p>Oops! Something went wrong on our end.</p>" in response_str

    assert status == '500 Internal server error'


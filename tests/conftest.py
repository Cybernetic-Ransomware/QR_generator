import base64
import io

import pytest

from app import app as flask_app, store


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def png_bytes():
    return base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQ'
        'AABjkB6QAAAABJRU5ErkJggg=='
    )


@pytest.fixture
def png_file(png_bytes):
    return io.BytesIO(png_bytes)


@pytest.fixture
def qr_token():
    token = store.put({'qr': b'fakeqr', 'artistic': None, 'artistic_ext': None})
    return token


@pytest.fixture
def qr_with_artistic_token():
    token = store.put({'qr': b'fakeqr', 'artistic': b'fakeart', 'artistic_ext': 'png'})
    return token

import io
from unittest.mock import MagicMock

from utils.mixins import NotificationMixin, MIN_SIZE, MAX_SIZE


class Validator(NotificationMixin):
    pass


v = Validator()


def _mock_file(data: bytes, filename: str = 'image.png'):
    f = MagicMock()
    f.filename = filename
    buf = io.BytesIO(data)
    f.read.side_effect = buf.read
    f.seek.side_effect = buf.seek
    return f


class TestValidateText:
    def test_empty_string_is_valid(self):
        ok, msg = v.validate_text('')
        assert ok is True
        assert msg == ''

    def test_55_chars_is_valid(self):
        ok, _ = v.validate_text('x' * 55)
        assert ok is True

    def test_56_chars_is_invalid(self):
        ok, msg = v.validate_text('x' * 56)
        assert ok is False
        assert '55' in msg


class TestValidateSize:
    def test_min_boundary(self):
        ok, _ = v.validate_size(MIN_SIZE)
        assert ok is True

    def test_max_boundary(self):
        ok, _ = v.validate_size(MAX_SIZE)
        assert ok is True

    def test_below_min(self):
        ok, msg = v.validate_size(MIN_SIZE - 1)
        assert ok is False
        assert str(MIN_SIZE) in msg
        assert str(MAX_SIZE) in msg

    def test_above_max(self):
        ok, msg = v.validate_size(MAX_SIZE + 1)
        assert ok is False
        assert str(MAX_SIZE) in msg


class TestValidateImage:
    def test_none_is_valid(self):
        ok, msg = v.validate_image(None)
        assert ok is True
        assert msg == ''

    def test_disallowed_extension(self):
        f = _mock_file(b'data', filename='image.bmp')
        ok, msg = v.validate_image(f)
        assert ok is False
        assert 'PNG' in msg or 'format' in msg.lower()

    def test_oversized_file(self):
        large = b'x' * (5 * 1024 * 1024 + 1)
        f = _mock_file(large, filename='image.png')
        ok, msg = v.validate_image(f)
        assert ok is False
        assert '5' in msg

    def test_seek_reset_after_size_check(self):
        data = b'x' * 100
        f = _mock_file(data, filename='image.png')
        v.validate_image(f)
        f.seek.assert_called_with(0)

    def test_valid_png(self):
        f = _mock_file(b'x' * 100, filename='image.png')
        ok, _ = v.validate_image(f)
        assert ok is True

    def test_gif_extension_allowed(self):
        f = _mock_file(b'x' * 100, filename='anim.gif')
        ok, _ = v.validate_image(f)
        assert ok is True

import io

import segno
from werkzeug.datastructures import FileStorage

from utils.mixins import ValidationMixin


class QRCodeGenerator(ValidationMixin):
    def __init__(self) -> None:
        self.qr_png: bytes | None = None
        self.artistic_png: bytes | None = None
        self.artistic_ext: str | None = None

    def generate_qr(
        self,
        text: str,
        size: int,
        image: FileStorage | None,
        color: str | None = None,
        bg_color: str = '#ffffff',
        micro: bool = False,
    ) -> tuple[bool, list[str]]:
        valid, errors = self.validate_data(text, size, image)
        if not valid:
            return False, errors

        try:
            qr = segno.make(text, micro=True) if micro else segno.make_qr(text)
        except segno.DataOverflowError:
            msg = 'Text is too long for a Micro QR code.' if micro else 'Text is too long for a QR code.'
            return False, [msg]

        buf = io.BytesIO()
        qr.save(buf, kind='png', scale=size, dark=color or 'black', light=bg_color)
        buf.seek(0)
        self.qr_png = buf.read()

        if image and image.filename:
            ext = 'gif' if image.filename.rsplit('.', 1)[-1].lower() == 'gif' else 'png'
            image.seek(0)
            art_buf = io.BytesIO()
            qr.to_artistic(background=image, target=art_buf, kind=ext, scale=size, dark=color or 'black', light=bg_color)
            art_buf.seek(0)
            self.artistic_png = art_buf.read()
            self.artistic_ext = ext

        return True, []

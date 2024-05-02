import segno

from utils.mixins import NotificationMixin
from werkzeug.datastructures import FileStorage


class QRCodeGenerator(NotificationMixin):
    def generate_qr(self, text: str, size: int, image: FileStorage | None, color: str | None = None) -> (bool, str):
        valid, errors = self.validate_data(text, size, image)

        if not valid:
            return False, errors

        qr = segno.make(text)
        extension = "png" if (extension := image.filename.split('.')[-1]) != "gif" else extension

        if color:
            qr.save(f'qr.png', scale=size, dark=color, light='white')
        else:
            qr.save(f'qr.png', scale=size)

        if image:
            qr.to_artistic(background=image, target=f'qr_with_image.{extension}', scale=size)

        return True, ""

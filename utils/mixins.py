from werkzeug.datastructures import FileStorage

MIN_SIZE = 1
MAX_SIZE = 30


class NotificationMixin:
    @staticmethod
    def validate_text(text: str) -> tuple[bool, str]:
        if len(text) > 55:
            return False, 'Text length should not exceed 55 characters.'
        return True, ''

    @staticmethod
    def validate_size(size: int) -> tuple[bool, str]:
        if not MIN_SIZE <= size <= MAX_SIZE:
            return False, f'Size should be between {MIN_SIZE} and {MAX_SIZE}.'
        return True, ''

    @staticmethod
    def validate_image(image: FileStorage | None) -> tuple[bool, str]:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if image and image.filename and image.filename.split('.')[-1].lower() not in allowed_extensions:
            return False, 'Image should be in PNG, JPG, JPEG, or GIF format.'
        if image:
            size_bytes = len(image.read())
            image.seek(0)
            if size_bytes > 5 * 1024 * 1024:  # 5 MB
                return False, 'Image size should not exceed 5 MB.'
        return True, ''

    def validate_data(self, text: str, size: int, image: FileStorage | None) -> tuple[bool, list[str]]:
        validations = [self.validate_text(text), self.validate_size(size), self.validate_image(image)]
        errors = [error for valid, error in validations if not valid]
        return len(errors) == 0, errors

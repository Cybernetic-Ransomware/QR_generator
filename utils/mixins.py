from werkzeug.datastructures import FileStorage


class NotificationMixin:
    @staticmethod
    def validate_text(text: str) -> (bool, str):
        if len(text) > 55:
            return False, "Text length should not exceed 55 characters."
        return True, ""

    @staticmethod
    def validate_size(size: int) -> (bool, str):
        if not 1 <= size <= 30:
            return False, "Size should be between 1 and 10."
        return True, ""

    @staticmethod
    def validate_image(image: FileStorage | None) -> (bool, str):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if image and image.filename.split('.')[-1].lower() not in allowed_extensions:
            return False, "Image should be in PNG, JPG, JPEG, or GIF format."
        if image and len(image.read()) > 5 * 1024 * 1024:  # 5 MB
            return False, "Image size should not exceed 5 MB."
        return True, ""

    def validate_data(self, text: str, size: int, image: FileStorage | None) -> (bool, list[str]):
        validations = [
            self.validate_text(text),
            self.validate_size(size),
            self.validate_image(image)
        ]
        errors = [error for valid, error in validations if not valid]
        return len(errors) == 0, errors

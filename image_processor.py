from PIL import ImageEnhance


class ImageProcessor:
    """Class to process and modify images."""
    @staticmethod
    def modify_image(image):
        # Example: Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.5)

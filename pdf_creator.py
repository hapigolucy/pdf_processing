from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


class PDFCreator:
    """Class to create a new PDF from extracted and modified images."""
    def __init__(self, output_pdf_path):
        self.output_pdf_path = output_pdf_path

    def save_images_to_new_pdf(self, images):
        c = canvas.Canvas(self.output_pdf_path, pagesize=letter)
        for page_num, img_index, img_obj, ext in images:
            buffer = BytesIO()
            img_obj.save(buffer, format="PNG")
            buffer.seek(0)
            c.drawImage(buffer, 0, 0, width=img_obj.width, height=img_obj.height)
            c.showPage()  # Start a new page for the next image
        c.save()

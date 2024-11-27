import fitz  # PyMuPDF
from io import BytesIO


class PDFReassembler:
    """Class to reassemble the PDF with modified images."""
    def __init__(self, original_pdf_path, output_pdf_path):
        self.original_pdf_path = original_pdf_path
        self.output_pdf_path = output_pdf_path

    def add_images_back_to_pdf(self, images):
        original_pdf = fitz.open(self.original_pdf_path)
        output_pdf = fitz.open()

        for page_num in range(len(original_pdf)):
            page = original_pdf[page_num]
            new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
            pixmap = page.get_pixmap()  # Render original page content
            
            # Add modified image for the current page
            for img_page_num, img_index, img_obj, ext in images:
                if img_page_num == page_num:
                    buffer = BytesIO()
                    img_obj.save(buffer, format="PNG")
                    buffer.seek(0)
                    new_page.insert_image(page.rect, stream=buffer.read())

        output_pdf.save(self.output_pdf_path)
        output_pdf.close()
        original_pdf.close()

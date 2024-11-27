import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO


class PDFImageExtractor:
    """Class to extract images and hyperlinks with text from a PDF."""
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_images(self):
        """Extract images from the PDF."""
        images = []
        pdf_document = fitz.open(self.pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                img_obj = Image.open(BytesIO(image_bytes))
                images.append((page_num, img_index, img_obj, image_ext))
        pdf_document.close()
        return images

    def extract_hyperlinks(self):
        """Extract hyperlinks and their associated text from the PDF."""
        hyperlinks = []
        pdf_document = fitz.open(self.pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            links = page.get_links()
            for link in links:
                if "uri" in link:
                    uri = link["uri"]
                    rect = link.get("from")  # Get the bounding rectangle of the link
                    if rect:
                        # Extract text within the bounding rectangle
                        text = page.get_textbox(rect).strip()
                    else:
                        text = None
                    hyperlinks.append((page_num, uri, text))
        pdf_document.close()
        return hyperlinks

    def extract_all(self):
        """Extract both images and hyperlinks."""
        images = self.extract_images()
        hyperlinks = self.extract_hyperlinks()
        return {"images": images, "hyperlinks": hyperlinks}

import pdfplumber

class PDFParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):

        text = ""

        with pdfplumber.open(self.file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text
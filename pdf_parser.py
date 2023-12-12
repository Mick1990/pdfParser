import fitz
import json

class PDFParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf_data = {}

    def __enter__(self):
        self.parse_pdf()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def parse_pdf(self):
        with fitz.open(self.file_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()

                lines = text.split('\n')
                if lines:
                    title = lines[0].strip()

                    page_data = {}
                    current_key = None
                    current_value = ""
                    for line in lines[1:]:
                        key_value = line.split(':')
                        if len(key_value) == 2:
                            if current_key is not None:
                                page_data[current_key] = current_value.strip()

                            current_key, current_value = key_value[0].strip(), key_value[1].strip()
                        else:
                            current_value += " " + line

                    if current_key is not None:
                        page_data[current_key] = current_value.strip()

                    # Использование заголовка в качестве ключа для словаря
                    self.pdf_data[title] = page_data

    def get_data(self):
        return self.pdf_data

file_path = 'test_task.pdf'

with PDFParser(file_path) as parser:
    result = parser.get_data()

formatted_json = json.dumps(result, indent=2)
print(formatted_json)

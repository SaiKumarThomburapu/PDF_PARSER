from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# load once
ocr_model = ocr_predictor(pretrained=True)

def run_doctr_on_page(pdf_path, page_idx):
    """
    Run DocTR OCR on a single page.
    """
    doc = DocumentFile.from_pdf(pdf_path)[page_idx:page_idx+1]
    result = ocr_model(doc)
    return result.export()


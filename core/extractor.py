import fitz  # PyMuPDF
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os

from core.utils import ensure_dir, save_json, log


def parse_pdf(pdf_path: str, output_dir: str):
    """
    Hybrid PDF Parser:
    - Extracts digital text (via PyMuPDF)
    - Runs OCR (via DocTR) for scanned/complex pages
    - Saves per-page JSON + global summary.json
    """

    # Prepare output folders
    ensure_dir(output_dir)
    pages_dir = ensure_dir(os.path.join(output_dir, "pages"))

    # Init OCR model once
    log("Loading DocTR OCR model...")
    ocr_model = ocr_predictor(pretrained=True)

    # Load PDF
    log(f"Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    doctr_doc = DocumentFile.from_pdf(pdf_path)

    all_pages = []

    for idx, page in enumerate(doc):
        log(f"Processing page {idx+1}/{len(doc)}...")

        # Try digital extraction
        text = page.get_text("text")

        if not text.strip():
            # Fallback to OCR
            log(f"Page {idx+1} seems scanned, running OCR...")
            ocr_result = ocr_model([doctr_doc[idx]]).export()

            # flatten text from blocks > lines > words
            words = []
            for block in ocr_result["pages"][0]["blocks"]:
                for line in block["lines"]:
                    for w in line["words"]:
                        words.append(w["value"])
            text = " ".join(words)

        # Save page-level JSON
        page_data = {"page_number": idx + 1, "text": text}
        save_json(page_data, os.path.join(pages_dir, f"page_{idx+1}.json"))

        all_pages.append(page_data)

    # Save summary JSON
    summary_path = os.path.join(output_dir, "summary.json")
    save_json(all_pages, summary_path)

    log(f"✅ Extraction finished. Outputs in: {output_dir}")
    return summary_path





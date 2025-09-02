import sys
import os
from core.extractor import parse_pdf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <path-to-pdf> [output-dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs"

    print(f"Extracting PDF: {pdf_path}")
    summary_path = parse_pdf(pdf_path, output_dir)
    print(f"✅ Extraction complete. Summary saved at: {summary_path}")



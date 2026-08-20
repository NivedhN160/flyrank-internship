import os
import pytest
from pdf_builder import PDFReportGenerator

def test_pdf_report_generation():
    generator = PDFReportGenerator(output_dir="test_reports")
    metrics = {
        "total_quotes": 100,
        "unique_authors": 50,
        "avg_quote_length": 142.5,
        "top_authors": [
            ("Albert Einstein", 10),
            ("J.K. Rowling", 9),
            ("Jane Austen", 5)
        ],
        "top_tags": [
            ("inspirational", 28),
            ("life", 26),
            ("love", 14)
        ],
        "sample_quotes": [
            {
                "author": "Albert Einstein",
                "quote": "The world as we have created it is a process of our thinking.",
                "tags": ["change", "deep-thoughts"]
            },
            {
                "author": "J.K. Rowling",
                "quote": "It is our choices that show what we truly are, far more than our abilities.",
                "tags": ["abilities", "choices"]
            }
        ]
    }
    pdf_path = generator.generate_pdf(job_id="test_job_101", metrics=metrics, title="Automated Backend Analytics Audit")
    
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 1000 # Valid multi-kilobyte PDF generated

    # Cleanup
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
            os.rmdir("test_reports")
        except Exception:
            pass

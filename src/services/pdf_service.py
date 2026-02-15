import requests
from core.config import get_settings

settings = get_settings()

def convert_html_to_pdf(html_content: str, output_pdf_file: str):
    response = requests.post(
        'https://api.pdfshift.io/v3/convert/pdf',
        headers={'X-API-Key': settings.pdfshift_api_key},
        json={
            'source': html_content,
            'format': 'A4',
            'margin': '15mm',
            'landscape': False,
            'use_print': False
        }
    )

    if response.status_code == 200:
        with open(output_pdf_file, 'wb') as f:
            f.write(response.content)
        return True
    else:
        response.raise_for_status()
        raise Exception(f"Failed to convert PDF: {response.text}")

def save_html_file(html_content: str, output_filename: str):
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(html_content)

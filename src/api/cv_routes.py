from fastapi import APIRouter, HTTPException
from schemas.cv import CVData
from services.gemini_service import generate_cv_with_gemini
from services.pdf_service import convert_html_to_pdf, save_html_file

router = APIRouter()

@router.post("/generate_cv/")
async def create_cv(cv_data: CVData):
    cv_dict = cv_data.model_dump()

    cv_html = generate_cv_with_gemini(cv_dict)
    
    if cv_html:
        html_filename = "generated_cv.html"
        pdf_filename = "generated_cv.pdf"
        
        save_html_file(cv_html, html_filename)
        try:
            convert_html_to_pdf(cv_html, pdf_filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

        return {
            "message": "CV generated successfully!", 
            "html_file": html_filename, 
            "pdf_file": pdf_filename
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to generate CV HTML.")

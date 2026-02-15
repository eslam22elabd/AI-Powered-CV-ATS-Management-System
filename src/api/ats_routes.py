import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ats_service import extract_text_from_pdf, analyze_cv_with_gemini

router = APIRouter()

@router.post("/analyze_cv/")
async def analyze_cv(file: UploadFile = File(...)):
    try:
        # Check if file is PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        # Save file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract and Analyze
        try:
            cv_text = extract_text_from_pdf(temp_path)
            analysis = analyze_cv_with_gemini(cv_text)
        finally:
            # Always delete temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        return {
            "message": "CV analyzed successfully",
            "filename": file.filename,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import PyPDF2
import json
from google import genai
from google.genai import types
from core.config import get_settings

settings = get_settings()

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def analyze_cv_with_gemini(cv_text: str) -> dict:
    client = genai.Client(api_key=settings.gemini_api_key)
    model = "gemini-3-flash-preview"

    prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer and HR professional. Your job is to evaluate resumes comprehensively and provide actionable insights.

Analyze the following CV/Resume and provide a detailed ATS score evaluation.

**CRITICAL INSTRUCTIONS:**
- You MUST respond with ONLY valid JSON format
- NO markdown formatting (no ```json or ```)
- NO explanations or additional text
- Start directly with the JSON object {{

**Scoring Methodology (Each out of 100):**

1. **Formatting Score (0-100):**
   - Structure clarity and readability (25 points)
   - ATS-friendly formatting (no images, tables, columns) (25 points)
   - Consistent formatting throughout (20 points)
   - Proper use of bullet points and white space (15 points)
   - Standard fonts and readable text size (15 points)

2. **Content Score (0-100):**
   - Clear, compelling summary/objective (20 points)
   - Quantifiable achievements with metrics (30 points)
   - Strong action verbs usage (15 points)
   - Relevant work experience descriptions (20 points)
   - Demonstrates impact and results (15 points)

3. **Keywords Score (0-100):**
   - Industry-specific technical skills (30 points)
   - Job-relevant terminology and buzzwords (25 points)
   - Tools, technologies, and frameworks mentioned (25 points)
   - Certifications and qualifications (10 points)
   - Soft skills keywords (10 points)

4. **Structure Score (0-100):**
   - Essential sections present (Contact, Summary, Experience, Education, Skills) (40 points)
   - Logical section ordering (20 points)
   - Completeness of information in each section (20 points)
   - Appropriate section titles (10 points)
   - Professional presentation (10 points)

**Overall Score Calculation:**
Average of all four scores (Formatting + Content + Keywords + Structure) / 4

**Response Format (STRICTLY JSON):**
{{
  "overall_score": <integer 0-100>,
  "formatting_score": <integer 0-100>,
  "content_score": <integer 0-100>,
  "keywords_score": <integer 0-100>,
  "structure_score": <integer 0-100>,
  "strengths": [
    "<specific strength with example>",
    "<specific strength with example>",
    "<specific strength with example>",
    "<specific strength with example>"
  ],
  "weaknesses": [
    "<specific weakness with explanation>",
    "<specific weakness with explanation>",
    "<specific weakness with explanation>",
    "<specific weakness with explanation>"
  ],
  "recommendations": [
    "<actionable recommendation 1>",
    "<actionable recommendation 2>",
    "<actionable recommendation 3>",
    "<actionable recommendation 4>",
    "<actionable recommendation 5>",
    "<actionable recommendation 6>"
  ],
  "detailed_analysis": {{
    "formatting": "<2-3 sentences about formatting quality and ATS compatibility>",
    "content": "<2-3 sentences about content quality and impact>",
    "keywords": "<2-3 sentences about keyword optimization and relevance>",
    "structure": "<2-3 sentences about structure and completeness>",
    "missing_sections": ["<section 1>", "<section 2>"],
    "strong_keywords_found": ["<keyword 1>", "<keyword 2>", "<keyword 3>", "<keyword 4>", "<keyword 5>"],
    "suggested_keywords": ["<missing keyword 1>", "<missing keyword 2>", "<missing keyword 3>", "<missing keyword 4>", "<missing keyword 5>"],
    "achievement_quality": "<assessment of how well achievements are quantified>",
    "ats_compatibility": "<overall assessment of ATS compatibility>"
  }}
}}

**Guidelines for Quality Analysis:**
- Be specific and constructive in feedback
- Provide actionable recommendations
- Identify concrete examples from the CV
- Focus on both technical and presentation aspects
- Consider modern hiring practices and ATS requirements
- Be honest but professional in assessment

**CV Content to Analyze:**

{cv_text}

**IMPORTANT:** Return ONLY the JSON object. Start immediately with {{
"""
                                
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig()

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text.strip()

    # Clean Response
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(response_text)
    except Exception as e:
        return {"error": f"Failed to parse response: {str(e)}", "raw_response": response_text}

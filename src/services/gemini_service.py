from google import genai
from google.genai import types
from core.config import get_settings

settings = get_settings()

def generate_cv_with_gemini(data: dict):
    client = genai.Client(api_key=settings.gemini_api_key)
    model = "gemini-3-flash-preview"

    prompt = f"""
You are an expert CV generator. Your goal is to create an EXACT visual replica of the professional CV layout provided below in HTML/CSS.

**LAYOUT INSTRUCTIONS (Follow precisely):**
1. **Header**: 
   - Name: Centered, Bold, ~24pt.
   - Job Title: Centered, Bold, ~16pt, dark gray.
   - Contact Row: Centered, ~11pt, gray. Format: "Email: {{email}} | Mobile: {{phone}} | Address: {{address}}" (Email should be a link).
   - Links Row: Centered, ~11pt, blue. Format: "LinkedIn | GitHub" (Both clickable links). Add space between them.
2. **Sections**: 
   - Headers (SUMMARY, PROFESSIONAL EXPERIENCE, EDUCATION, COURSES, etc.): Uppercase, Bold, ~14pt.
   - Header Separation: A thin light-gray horizontal line (`border-bottom: 1px solid #ccc;`) directly below the text covering full width.
3. **Experience & Courses**:
   - Header Line: Bold Job Title/Course Name on the left. Dates on the right. Both on the same line.
   - Sub-line (for experience): Company Name in normal font or slightly lighter.
   - Bullet Points: Simple dots, indented.
4. **Dates**: Always right-aligned on the same line as the title of the entry (Job Title or Course Name). Use flexbox (`display: flex; justify-content: space-between;`) for these lines.
5. **Typography & Colors**: 
   - Font: Use a clean sans-serif like 'Segoe UI', 'Arial', or 'Inter'.
   - Body text: ~11pt.
   - All links: Blue and underlined.
6. **Page**: A4 size, 10mm margins. No background colors.

**Summary Generation Rule**:
Analyze Skills, Experience, Education, and Courses. Write a compelling 3-4 sentence professional summary that highlights the candidate's core expertise in {data['job_title']} based ON THE PROVIDED DATA. Write it as the candidate.

**Candidate Data:**
Name: {data['name']}
Job Title: {data['job_title']}
Email: {data['email']}
Phone: {data['phone']}
Address: {data['address']}
LinkedIn: {data['linkedin']}
GitHub: {data['github']}
Skills: {', '.join(data['skills'])}
Experience: {data['experience']}
Education: {data['education']}
Courses: {data['courses']}
Languages: {data['languages']}

**CRITICAL: Output ONLY valid HTML. No markdown, no code blocks, no backticks.**

Generate the HTML now:
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig()

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    if not response or not response.text:
        return None

    response_text = response.text.strip()

    # Clean HTML from markdown formatting
    response_text = response_text.replace("```html", "").replace("```", "").strip()
    
    return response_text

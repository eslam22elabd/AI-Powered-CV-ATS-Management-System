# AI-Powered CV & ATS Management System 🚀

A professional, modularized FastAPI system designed to generate ATS-optimized resumes and provide deep analytical CV scoring using **Gemini 3 Flash Preview** by way ATS .

## 🏗️ Project Structure

The project follows a clean, modular architecture for scalability and maintainability:

```text
src/
├── api/             # Route handlers (CV & ATS endpoints)
├── core/            # Configuration and environment settings
├── schemas/         # Pydantic models for data validation
├── services/        # Business logic (Gemini, ATS, PDF conversion)
└── main.py          # Application entry point
```

## 🌟 Key Features

### 1. CV Generation Service
- **Gemini 3 Integration**: Uses the latest thinking-capable models to craft professional content.
- **Dynamic Summaries**: Automatically generates a context-aware professional summary based on candidate track.
- **Expert Layout**: Produces full-width, professional HTML resumes.
- **PDF Conversion**: Seamlessly converts HTML to PDF via the **PDF Shift API**.

### 2. ATS Analysis Service
- **Deep Scoring**: Evaluates parseability, content impact, and keyword density.
- **Actionable Insights**: identifies specific strengths, weaknesses, and missing critical skills.
- **Improvement Roadmap**: Provides concrete steps for candidates to improve their hiring chances.

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **AI Model**: Google Gemini 3 Flash Preview
- **PDF Engine**: PDF Shift API
- **Settings Management**: Pydantic Settings (Environment-based)
- **PDF Parsing**: PyPDF2

## ⚙️ Installation & Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
   ```bash
   python==3.14.0
   pip install -r src/requirments.txt
   ```

## 🚀 Running the Application

### Method 1: Python Directly
```bash
cd src
uvicorn main:app --reload
```

### Method 2: Docker (Recommended)
Containerization makes deployment much easier:

1. **Build the Image**:
   ```bash
   docker build -t cv-system .
   ```
2. **Run the Container**:
   ```bash
   docker run -p 8000:8000 --env-file src/.env cv-system
   ```

## 📖 API Documentation
Once the server is running, you can access the interactive documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)


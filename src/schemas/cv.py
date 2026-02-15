from pydantic import BaseModel
from typing import List

class CVData(BaseModel):
    name: str
    job_title: str
    email: str
    phone: str
    address: str
    linkedin: str
    github: str
    skills: List
    experience: List
    education: List
    courses: List
    languages: str

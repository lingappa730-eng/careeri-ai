import re

ALL_SKILLS = ["Python","SQL","Excel","Power BI","Tableau","HTML","CSS","JavaScript","React","Django","Machine Learning","Statistics","Git","Figma","Photoshop","Java","C++","API","AWS","UI Design"]

def extract_text_from_pdf(file):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return ""

def extract_text_from_docx(file):
    try:
        import docx
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return ""

def extract_skills(text):
    found = []
    if not text:
        return found
    text_lower = text.lower()
    for skill in ALL_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return found

def analyze_job_description(jd_text, resume_skills):
    jd_skills = extract_skills(jd_text or "")
    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    match = round(len(matched)/len(jd_skills)*100, 2) if jd_skills else 0
    return {"jd_skills": jd_skills, "matched": matched, "missing": missing, "match": match}

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def load_careers():
    # Try both places - careers.json in main folder OR data/careers.json
    if os.path.exists('careers.json'):
        path = 'careers.json'
    elif os.path.exists('data/careers.json'):
        path = 'data/careers.json'
    else:
        path = 'careers.json'
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def recommend_careers(user_skills_list):
    careers = load_careers()
    user_skills = set([s.strip().lower() for s in user_skills_list if s and s.strip()])
    user_text = " ".join(user_skills)
    results = []
    for career in careers:
        required = [s.lower() for s in career.get('skills', [])]
        required_set = set(required)
        have = [s for s in career.get('skills', []) if s.lower() in user_skills]
        missing = [s for s in career.get('skills', []) if s.lower() not in user_skills]
        match_percent = (len(have) / len(required_set) * 100) if required_set else 0
        job_text = " ".join(required)
        try:
            if not user_text.strip() or not job_text.strip():
                tfidf_score = 0
            else:
                vec = TfidfVectorizer().fit_transform([user_text, job_text])
                tfidf_score = float(cosine_similarity(vec[0], vec[1])[0][0] * 100)
        except Exception:
            tfidf_score = 0
        final_score = round(match_percent * 0.7 + tfidf_score * 0.3, 2)
        results.append({
            "career": career.get('title', 'Unknown Career'),
            "match": final_score,
            "have": have,
            "missing": missing,
            "have_count": len(have),
            "total": len(required),
            "salary": career.get('salary', 'Not Mentioned'),
            "demand": career.get('demand', 'Medium'),
            "roadmap": career.get('roadmap', ['Learn missing skills step by step', 'Do practice projects', 'Build portfolio and apply'])
        })
    results = sorted(results, key=lambda x: x['match'], reverse=True)
    return results[:5]

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def load_careers():
    with open('data/careers.json', encoding='utf-8') as f:
        return json.load(f)

def recommend_careers(user_skills_list):
    careers = load_careers()
    user_skills = set([s.strip().lower() for s in user_skills_list if s.strip()])
    user_text = " ".join(user_skills)
    results = []
    for career in careers:
        required = [s.lower() for s in career['skills']]
        required_set = set(required)
        have = [s for s in career['skills'] if s.lower() in user_skills]
        missing = [s for s in career['skills'] if s.lower() not in user_skills]
        match_percent = (len(have) / len(required_set) * 100) if required_set else 0
        job_text = " ".join(required)
        try:
            vec = TfidfVectorizer().fit_transform([user_text, job_text])
            tfidf_score = float(cosine_similarity(vec[0], vec[1])[0][0] * 100)
        except:
            tfidf_score = 0
        final_score = round(match_percent * 0.7 + tfidf_score * 0.3, 2)
        results.append({
            "career": career['title'],
            "match": final_score,
            "have": have,
            "missing": missing,
            "have_count": len(have),
            "total": len(required),
            "salary": career['salary'],
            "demand": career['demand'],
            "roadmap": career['roadmap']
        })
    results = sorted(results, key=lambda x: x['match'], reverse=True)
    return results[:5]
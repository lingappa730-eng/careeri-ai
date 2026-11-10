from flask import Flask, request, jsonify, render_template
from model import recommend_careers
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills, analyze_job_description
import urllib.parse

app = Flask(__name__)

# 💯 MODULE 7 - LEARN 100% - PARTICULAR WEBSITES (BACKEND)
# Video + Free Course + Practice - For Every Skill
LEARN_WEBSITES = {
    "video": [
        {"name": "YouTube - CodeWithHarry", "url": "https://www.youtube.com/@CodeWithHarry"},
        {"name": "YouTube - Apna College", "url": "https://www.youtube.com/@ApnaCollegeOfficial"},
        {"name": "YouTube - freeCodeCamp", "url": "https://www.youtube.com/@freecodecamp"},
    ],
    "free_course": [
        {"name": "NPTEL - Free Course + Certificate", "url": "https://www.nptel.ac.in/courses"},
        {"name": "Great Learning - Free", "url": "https://www.mygreatlearning.com/"},
        {"name": "Coursera", "url": "https://www.coursera.org/"},
        {"name": "edX", "url": "https://www.edx.org/"},
        {"name": "W3Schools", "url": "https://www.w3schools.com/"},
    ],
    "practice": [
        {"name": "HackerRank - Practice", "url": "https://www.hackerrank.com/"},
        {"name": "Kaggle - Projects", "url": "https://www.kaggle.com/learn"},
        {"name": "LeetCode - Practice", "url": "https://leetcode.com/"},
        {"name": "GitHub - Projects", "url": "https://github.com/"},
    ]
}

def get_learn_links(skill, career=""):
    # Make skill-wise direct links - e.g. Statistics -> YouTube Search Statistics CodeWithHarry
    q = urllib.parse.quote(f"{skill} CodeWithHarry")
    qc = urllib.parse.quote(skill)
    qg = urllib.parse.quote(skill.lower())
    return {
        "skill": skill,
        "career": career,
        "video": [
            {"name": f"YouTube - Learn {skill} - CodeWithHarry / Apna College", "url": f"https://www.youtube.com/results?search_query={q}"},
            {"name": "YouTube - Apna College", "url": "https://www.youtube.com/@ApnaCollegeOfficial"},
            {"name": "YouTube - freeCodeCamp", "url": "https://www.youtube.com/@freecodecamp"},
        ],
        "free_course": [
            {"name": "NPTEL Free Course", "url": "https://www.nptel.ac.in/courses"},
            {"name": "Great Learning Free", "url": "https://www.mygreatlearning.com/"},
            {"name": f"Coursera - {skill}", "url": f"https://www.coursera.org/search?query={qc}"},
            {"name": "edX", "url": "https://www.edx.org/"},
        ],
        "practice": [
            {"name": "HackerRank Practice", "url": "https://www.hackerrank.com/"},
            {"name": "Kaggle Projects", "url": "https://www.kaggle.com/learn"},
            {"name": f"GitHub - {skill} Projects", "url": f"https://github.com/topics/{qg}"},
        ],
        "plan": [
            "Week 1-2: Watch Video + NPTEL",
            "Week 3-4: HackerRank Practice",
            "Week 5-6: Kaggle / GitHub - 2 Projects",
            "Week 7-8: Revise + Mock Interview = 100% Ready"
        ]
    }

# ===== ROUTES =====
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.is_json:
        data = request.get_json()
        skills_text = data.get('skills', '')
        skills_list = [s.strip() for s in skills_text.split(',') if s.strip()]
        if not skills_list:
            return jsonify({"error": "Please enter at least 1 skill"}), 400
        results = recommend_careers(skills_list)
        # 💯 Add Learn 100% links to every career - Backend
        for r in results:
            r['learn_100'] = [get_learn_links(m, r['career']) for m in r.get('missing', [])]
            r['learn_websites'] = LEARN_WEBSITES
        return jsonify(results)
    skills_input = request.form.get('skills', '')
    skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
    return render_template('home.html', results=recommend_careers(skills_list), skills_input=skills_input)

# 💯 NEW API - /learn/Statistics - Returns Particular Websites for 1 Skill
@app.route('/learn/<skill>', methods=['GET'])
def learn_skill(skill):
    career = request.args.get('career', '')
    return jsonify(get_learn_links(skill, career))

# 💯 NEW API - /learn_websites - Returns All Particular Websites
@app.route('/learn_websites', methods=['GET'])
def learn_websites():
    return jsonify(LEARN_WEBSITES)

# MODULE 1,2,3,4,5,6 - RESUME + JD ANALYSIS
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    jd_text = request.form.get('job_description', '')
    if not file:
        return jsonify({"error": "Please upload resume"}), 400
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    else:
        return jsonify({"error": "Only PDF / DOCX allowed"}), 400
    skills = extract_skills(text)
    jd_result = analyze_job_description(jd_text, skills) if jd_text else None
    jobs = recommend_careers(skills)
    # 💯 Add Learn links to resume jobs also
    for r in jobs:
        r['learn_100'] = [get_learn_links(m, r['career']) for m in r.get('missing', [])]
    return jsonify({
        "extracted_text": text[:1000],
        "skills_found": skills,
        "jd_analysis": jd_result,
        "job_recommendations": jobs,
        "learn_websites": LEARN_WEBSITES
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
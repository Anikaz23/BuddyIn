from itertools import chain
from services.ai.openai_model import OpenAIModel

openai_model = OpenAIModel()

def give_resume_score(resume, r_description):
    if not resume or not r_description:
        return "Insufficient data to calculate score.", 400

    resume = resume.lower()

    skills_list = list(chain.from_iterable(r_description[skills_section] for skills_section in r_description.values() if isinstance(r_description[skills_section], list)))
    experience_required = r_description.get("experience", "").lower()
    degree_required = r_description.get("degree", "").lower()

    matched_skills = sum(1 for skill in skills_list if skill.lower() in resume)
    skill_score = (matched_skills / len(skills_list)) * 100 if skills_list else 0
    experience_degree_match = openai_model.match_resume(experience_required, degree_required, resume)

    if experience_degree_match.get("experience_match", False)  and experience_degree_match.get("degree_match", False):
        return skill_score

    message = ""
    if not experience_degree_match.get("experience_match", False):
        error_message += "Experience requirement not met. "
    if not experience_degree_match.get("degree_match", False):
        error_message += "Degree requirement not met."

    return message
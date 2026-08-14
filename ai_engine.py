CAREERS = {
    "Cybersecurity Engineer": {
        "skills": {
            "python": 20,
            "linux": 20,
            "networking": 20,
            "cybersecurity": 25,
            "ethical hacking": 15
        }
    },

    "Cloud Engineer": {
        "skills": {
            "linux": 20,
            "networking": 20,
            "python": 15,
            "cloud": 30,
            "devops": 15
        }
    },

    "Data Scientist": {
        "skills": {
            "python": 25,
            "statistics": 20,
            "machine learning": 30,
            "sql": 15,
            "data analysis": 10
        }
    },

    "Web Developer": {
        "skills": {
            "html": 20,
            "css": 20,
            "javascript": 25,
            "python": 15,
            "sql": 20
        }
    }
}


def recommend_careers(user_skills, interests):

    user_skills = [skill.lower() for skill in user_skills]
    interests = [interest.lower() for interest in interests]

    results = []

    for career, data in CAREERS.items():

        score = 0
        matched = []
        missing = []

        for skill, weight in data["skills"].items():

            if skill in user_skills:
                score += weight
                matched.append(skill)
            else:
                missing.append(skill)

        # Interest bonus
        career_lower = career.lower()

        for interest in interests:
            if interest in career_lower:
                score += 10

        results.append({
            "career": career,
            "score": min(score, 100),
            "matched_skills": matched,
            "missing_skills": missing
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results
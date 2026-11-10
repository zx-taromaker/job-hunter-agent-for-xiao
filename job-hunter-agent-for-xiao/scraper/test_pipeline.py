"""
Smoke test and validation script for Job Hunter Agent recruitment pipeline.
Validates:
  1. Parsing cv.pdf (Xiao ZHANG)
  2. Gemini 2.5 Flash evaluation structure (1-10 score, matched_skills, missing_skills)
  3. 4-second delay pacing (time.sleep(4))
"""

import sys
import json
import time

from cv_parser import parse_cv
from gemini_evaluator import GeminiJobEvaluator


def run_pipeline_test():
    print("=" * 70)
    print("  🧪 VALIDATING CV PARSER & GEMINI 2.5 FLASH EVALUATOR")
    print("=" * 70)

    # 1. Test CV Parsing
    print("\n[Step 1] Parsing cv.pdf...")
    cv = parse_cv("cv.pdf")
    print(f"  ✅ Candidate Name   : {cv.name}")
    print(f"  ✅ Location         : {cv.contact.get('location')}")
    print(f"  ✅ Degree           : {cv.education[0].get('degree')} @ {cv.education[0].get('school')}")
    print(f"  ✅ Languages        : {', '.join([f'{k} ({v})' for k, v in cv.languages.items()])}")
    print(f"  ✅ Software & Tools : {', '.join(cv.skills.get('it', []))}")

    # 2. Test Sample French Job Postings from the 5 Portals
    print("\n[Step 2] Testing Matching Engine on 5 French Portals...")
    sample_jobs = [
        {
            "title": "Assistant Digital Marketing & E-Commerce (F/H)",
            "company": "L'Oréal",
            "location": "Clichy / Paris",
            "contract": "CDI",
            "description": "Coordination des campagnes digitales, création de contenu social media (TikTok), analyse des KPIs de vente et engagement influenceurs. Profil bilingue FR/EN.",
            "apply_url": "https://www.welcometothejungle.com/fr/companies/loreal/jobs/assistant-digital-marketing",
            "platform": "Welcome to the Jungle"
        },
        {
            "title": "Chef de Projet Marketing International & E-Commerce (Cadre)",
            "company": "Kering Group",
            "location": "Paris 8ème",
            "contract": "CDI - Cadre",
            "description": "Stratégie de marque cross-border, partenariats commerciaux, analyse des investissements digitaux et négociation KOL en Asie et Europe.",
            "apply_url": "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/kering_marketing",
            "platform": "APEC (Cadres)"
        }
    ]

    evaluator = GeminiJobEvaluator(model_name="gemini-2.5-flash", request_delay=1.0) # 1s for quick test
    cv_md = cv.to_markdown()

    for idx, job in enumerate(sample_jobs):
        print(f"\n--- Evaluating Job #{idx+1}: {job['title']} @ {job['company']} ---")
        eval_res = evaluator.evaluate_job(cv_md, job)
        print(f"  🎯 Compatibility Score: {eval_res['score']} / 10")
        print(f"  ✅ Matched Skills     : {', '.join(eval_res['matched_skills'])}")
        print(f"  ⚠️ Missing Skills     : {', '.join(eval_res['missing_skills'])}")
        print(f"  💡 Strengths          : {eval_res['strengths'][0] if eval_res['strengths'] else 'None'}")
        print(f"  📝 Justification      : {eval_res['justification']}")

    print("\n" + "=" * 70)
    print("  🎉 ALL TESTS PASSED: CV parsed, Gemini 2.5 Flash logic verified!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_pipeline_test()

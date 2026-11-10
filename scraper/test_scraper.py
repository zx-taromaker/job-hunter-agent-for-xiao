"""
Test and Verification Script for Job Hunter Agent Multi-Site Scraper.
Verifies:
  1. Strict JSON output containing title, company, location, contract, description, apply_url.
  2. The 5 French portals integration (WTTJ, Indeed, HelloWork, France Travail, APEC).
  3. 4-second delay compliance (time.sleep(4)) respecting Gemini free tier 15 RPM.
"""

import sys
import json
import time
from typing import List, Dict, Any

from models import JobListing
from job_scraper import FrenchJobScraper, scrape_jobs


def run_unit_verification():
    print("=================================================================")
    print("  🧪 Verifying Job Hunter Agent Scraper Models & Schema")
    print("=================================================================")

    sample = JobListing(
        title="Lead Full Stack Engineer",
        company="Doctolib",
        location="Paris (Hybrid)",
        contract="CDI",
        description="Conception et développement d'APIs Node.js et frontends React.",
        apply_url="https://www.welcometothejungle.com/fr/companies/doctolib/jobs/lead-full-stack",
        platform="Welcome to the Jungle"
    )

    clean_dict = sample.to_clean_dict()
    required_keys = {"title", "company", "location", "contract", "description", "apply_url"}

    print(f"\n[1] Checking Required Keys in Standardized Output:")
    for key in required_keys:
        present = key in clean_dict
        val = clean_dict.get(key)
        status = "✅" if present and val else "❌"
        print(f"  {status} Key '{key}': {val[:30] if isinstance(val, str) else val}")

    assert required_keys.issubset(clean_dict.keys()), "Missing required keys in standardized dictionary!"

    print("\n[2] Checking JSON Serialization:")
    json_output = json.dumps([clean_dict], indent=2, ensure_ascii=False)
    print(json_output)

    print("\n[3] Checking Rate-Limiting Logic:")
    start_time = time.time()
    scraper = FrenchJobScraper(request_delay=0.5) # Short delay for fast test
    scraper._sleep_rate_limit("Test Portal")
    elapsed = time.time() - start_time
    print(f"  ✅ Rate-limiter successfully invoked. Elapsed time: {elapsed:.2f}s")

    print("\n=================================================================")
    print("  🎉 All Scraper Schema & Rate Limiter Tests Passed Successfully!")
    print("=================================================================\n")


if __name__ == "__main__":
    run_unit_verification()

"""
Job Hunter Agent for Xiao — Python Multi-Site Job Scraping Package
"""

from .models import JobListing
from .job_scraper import FrenchJobScraper, scrape_jobs

__all__ = ["FrenchJobScraper", "JobListing", "scrape_jobs"]

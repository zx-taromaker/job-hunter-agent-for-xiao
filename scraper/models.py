"""
Standardized Job Listing Data Models for Job Hunter Agent for Xiao.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class JobListing:
    """
    Standardized job listing schema matching the exact challenge requirements:
    - title: Job title
    - company: Hiring company name
    - location: City / Region / Remote status
    - contract: CDI, CDD, Freelance, Cadre, etc.
    - description: Extracted text summary or full job description
    - apply_url: Direct application URL
    """
    title: str
    company: str
    location: str
    contract: str
    description: str
    apply_url: str
    platform: Optional[str] = None
    salary: Optional[str] = None
    date_posted: Optional[str] = None
    scraped_at: Optional[str] = None

    def __post_init__(self):
        if not self.scraped_at:
            self.scraped_at = datetime.utcnow().isoformat() + "Z"
        # Sanitize text
        self.title = (self.title or "").strip()
        self.company = (self.company or "Confidential").strip()
        self.location = (self.location or "France").strip()
        self.contract = (self.contract or "Non spécifié").strip()
        self.description = (self.description or "").strip()
        self.apply_url = (self.apply_url or "").strip()

    def to_dict(self) -> Dict[str, Any]:
        """Returns standard dictionary containing all standardized fields."""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "contract": self.contract,
            "description": self.description,
            "apply_url": self.apply_url,
            "platform": self.platform,
            "salary": self.salary,
            "date_posted": self.date_posted,
            "scraped_at": self.scraped_at,
        }

    def to_clean_dict(self) -> Dict[str, Any]:
        """Returns strictly the 6 core required fields."""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "contract": self.contract,
            "description": self.description,
            "apply_url": self.apply_url,
        }

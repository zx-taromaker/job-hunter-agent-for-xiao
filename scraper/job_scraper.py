"""
=============================================================================
Job Hunter Agent for Xiao — Python Multi-Site Job Scraping Module
Target Portals:
  1. Welcome to the Jungle (wttj)
  2. Indeed France (indeed)
  3. HelloWork (hellowork)
  4. France Travail (francetravail)
  5. APEC (apec)

Anti-Bot & Rate-Limiting Strategy:
  - Uses robust libraries (JobSpy / cloudscraper / public REST / Algolia endpoints)
  - Employs realistic browser headers and JSON-LD schema parsing
  - Strictly enforces time.sleep(4) between requests to honor Gemini's 15 RPM free tier
=============================================================================
"""

import sys
import json
import time
import logging
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus

# HTTP and parsing libraries (standard / robust fallbacks)
try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Optional JobSpy integration for Indeed / LinkedIn
try:
    from jobspy import scrape_jobs
    HAS_JOBSPY = True
except ImportError:
    HAS_JOBSPY = False

from .models import JobListing

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("JobHunterScraper")

# Realistic desktop browser headers
COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}


class FrenchJobScraper:
    """
    Multi-site scraper tailored for French job boards, designed for Xiao's job hunting pipeline.
    """

    def __init__(self, request_delay: float = 4.0):
        """
        :param request_delay: Delay in seconds between requests (default 4.0s for 15 RPM Gemini compliance)
        """
        self.request_delay = request_delay
        self.session = requests.Session() if requests else None
        if self.session:
            self.session.headers.update(COMMON_HEADERS)

    def _sleep_rate_limit(self, context: str = ""):
        """
        Respects Gemini free tier (15 RPM limit = 60s / 15 = 4.0s minimum gap).
        """
        msg = f"⏳ [RateLimiter] Sleeping {self.request_delay}s to respect Gemini 15 RPM limit..."
        if context:
            msg += f" (after {context})"
        logger.info(msg)
        time.sleep(self.request_delay)

    # -------------------------------------------------------------------------
    # 1. Welcome to the Jungle (WTTJ)
    # -------------------------------------------------------------------------
    def scrape_wttj(self, query: str, location: str = "Paris", limit: int = 10) -> List[JobListing]:
        """
        Scrapes Welcome to the Jungle via public Next.js / Algolia endpoints or HTML JSON-LD.
        """
        logger.info(f"🔍 [WTTJ] Scraping Welcome to the Jungle for '{query}' in '{location}'...")
        results: List[JobListing] = []

        if not self.session:
            logger.warning("[WTTJ] Requests library not available.")
            return results

        try:
            # WTTJ uses Next.js with server-rendered state and public API endpoints
            encoded_query = quote_plus(query)
            encoded_loc = quote_plus(location)
            url = f"https://www.welcometothejungle.com/fr/jobs?query={encoded_query}&aroundQuery={encoded_loc}&page=1"

            resp = self.session.get(url, timeout=12)
            if resp.status_code == 200:
                html = resp.text
                # Method A: Extract __NEXT_DATA__ embedded JSON
                next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
                if next_data_match:
                    try:
                        data = json.loads(next_data_match.group(1))
                        # Inspect queries / algolia state
                        dehydrated = data.get("props", {}).get("pageProps", {}).get("dehydratedState", {})
                        queries = dehydrated.get("queries", [])
                        for q in queries:
                            hits = q.get("state", {}).get("data", {}).get("hits", [])
                            for hit in hits[:limit]:
                                title = hit.get("name") or hit.get("title") or "Poste Tech"
                                company = hit.get("organization", {}).get("name") or "Startup WTTJ"
                                loc_name = hit.get("office", {}).get("city") or location
                                contract_type = hit.get("contract_type", "CDI")
                                desc = hit.get("summary") or hit.get("description") or f"Rôle chez {company}"
                                slug = hit.get("slug")
                                org_slug = hit.get("organization", {}).get("slug")
                                apply_url = f"https://www.welcometothejungle.com/fr/companies/{org_slug}/jobs/{slug}" if (org_slug and slug) else url

                                results.append(JobListing(
                                    title=title,
                                    company=company,
                                    location=f"{loc_name} (France)",
                                    contract=contract_type.upper(),
                                    description=desc,
                                    apply_url=apply_url,
                                    platform="Welcome to the Jungle"
                                ))
                    except Exception as e:
                        logger.debug(f"[WTTJ] NEXT_DATA parse error: {e}")

                # Method B: Fallback HTML card parsing
                if not results and BeautifulSoup:
                    soup = BeautifulSoup(html, "html.parser")
                    articles = soup.find_all("li", attrs={"data-testid": re.compile(r"search-results-list-item")}) or soup.find_all("article")
                    for article in articles[:limit]:
                        title_el = article.find("h4") or article.find("h3") or article.find("a")
                        company_el = article.find("span", class_=re.compile(r"company|organization", re.I))
                        link_el = article.find("a", href=True)
                        if title_el:
                            title = title_el.get_text(strip=True)
                            company = company_el.get_text(strip=True) if company_el else "WTTJ Company"
                            apply_url = "https://www.welcometothejungle.com" + link_el["href"] if link_el and link_el["href"].startswith("/") else (link_el["href"] if link_el else url)
                            results.append(JobListing(
                                title=title,
                                company=company,
                                location=location,
                                contract="CDI",
                                description=f"Offre d'emploi WTTJ pour {title} chez {company}.",
                                apply_url=apply_url,
                                platform="Welcome to the Jungle"
                            ))
            else:
                logger.warning(f"[WTTJ] HTTP status {resp.status_code}")

        except Exception as e:
            logger.error(f"[WTTJ] Error: {e}")

        logger.info(f"✅ [WTTJ] Found {len(results)} listings.")
        self._sleep_rate_limit("Welcome to the Jungle")
        return results

    # -------------------------------------------------------------------------
    # 2. Indeed France (indeed)
    # -------------------------------------------------------------------------
    def scrape_indeed(self, query: str, location: str = "Paris", limit: int = 10) -> List[JobListing]:
        """
        Scrapes Indeed France.
        Strategy:
          1. Uses JobSpy if installed (bypasses Cloudflare 403 via TLS client spoofing).
          2. Fallback to Indeed public RSS/XML feed (zero bot block, highly reliable).
        """
        logger.info(f"🔍 [Indeed] Scraping Indeed France for '{query}' in '{location}'...")
        results: List[JobListing] = []

        # Strategy 1: JobSpy
        if HAS_JOBSPY:
            try:
                logger.info("[Indeed] Using python-jobspy engine...")
                jobs_df = scrape_jobs(
                    site_name=["indeed"],
                    search_term=query,
                    location=location,
                    results_wanted=limit,
                    country_indeed="france"
                )
                if jobs_df is not None and not jobs_df.empty:
                    for _, row in jobs_df.iterrows():
                        results.append(JobListing(
                            title=str(row.get("title", "Poste")),
                            company=str(row.get("company", "Entreprise")),
                            location=str(row.get("location", location)),
                            contract=str(row.get("job_type", "CDI")),
                            description=str(row.get("description", ""))[:500],
                            apply_url=str(row.get("job_url", "https://fr.indeed.com")),
                            platform="Indeed France",
                            salary=str(row.get("min_amount", "")) if row.get("min_amount") else None
                        ))
                    logger.info(f"✅ [Indeed] JobSpy retrieved {len(results)} listings.")
                    self._sleep_rate_limit("Indeed (JobSpy)")
                    return results
            except Exception as e:
                logger.warning(f"[Indeed] JobSpy encountered error: {e}. Switching to RSS fallback.")

        # Strategy 2: Public Indeed RSS/XML feed
        if self.session:
            try:
                encoded_query = quote_plus(query)
                encoded_loc = quote_plus(location)
                rss_url = f"https://fr.indeed.com/rss?q={encoded_query}&l={encoded_loc}"
                
                resp = self.session.get(rss_url, timeout=12)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    channel = root.find("channel")
                    if channel:
                        items = channel.findall("item")
                        for item in items[:limit]:
                            title = item.findtext("title", "Poste")
                            link = item.findtext("link", "https://fr.indeed.com")
                            source = item.findtext("source", "Entreprise Indeed")
                            desc = item.findtext("description", "")
                            # Clean HTML tags in description
                            clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()

                            results.append(JobListing(
                                title=title,
                                company=source,
                                location=location,
                                contract="CDI",
                                description=clean_desc,
                                apply_url=link,
                                platform="Indeed France"
                            ))
                else:
                    logger.warning(f"[Indeed RSS] Status {resp.status_code}")
            except Exception as e:
                logger.error(f"[Indeed RSS] Error: {e}")

        logger.info(f"✅ [Indeed] Found {len(results)} listings.")
        self._sleep_rate_limit("Indeed")
        return results

    # -------------------------------------------------------------------------
    # 3. HelloWork (hellowork)
    # -------------------------------------------------------------------------
    def scrape_hellowork(self, query: str, location: str = "Paris", limit: int = 10) -> List[JobListing]:
        """
        Scrapes HelloWork (formerly RegionsJob), France's leading employment board.
        Strategy: Extracts structured JSON-LD schema (type: JobPosting) or HTML offer cards.
        """
        logger.info(f"🔍 [HelloWork] Scraping HelloWork for '{query}' in '{location}'...")
        results: List[JobListing] = []

        if not self.session:
            return results

        try:
            encoded_query = quote_plus(query)
            encoded_loc = quote_plus(location)
            url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={encoded_query}&l={encoded_loc}"

            headers = dict(COMMON_HEADERS)
            headers["Referer"] = "https://www.hellowork.com/fr-fr/"

            resp = self.session.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                html = resp.text

                # Method A: Extract Schema.org JSON-LD
                json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
                for block in json_ld_matches:
                    try:
                        data = json.loads(block)
                        items = data if isinstance(data, list) else [data]
                        for item in items:
                            if item.get("@type") == "JobPosting":
                                title = item.get("title")
                                company = item.get("hiringOrganization", {}).get("name") or "HelloWork Client"
                                loc_obj = item.get("jobLocation", {}).get("address", {})
                                loc = loc_obj.get("addressLocality") or location
                                contract = item.get("employmentType") or "CDI"
                                desc = re.sub(r"<[^>]+>", " ", item.get("description", "")).strip()
                                apply_url = item.get("url") or url

                                results.append(JobListing(
                                    title=title,
                                    company=company,
                                    location=loc,
                                    contract=contract,
                                    description=desc[:500],
                                    apply_url=apply_url,
                                    platform="HelloWork"
                                ))
                                if len(results) >= limit:
                                    break
                    except Exception:
                        continue

                # Method B: Parse HTML offer cards if JSON-LD wasn't populated
                if not results and BeautifulSoup:
                    soup = BeautifulSoup(html, "html.parser")
                    cards = soup.find_all("div", attrs={"data-offer-id": True}) or soup.find_all("li", class_=re.compile(r"offer", re.I))
                    for card in cards[:limit]:
                        title_el = card.find("h3") or card.find("a")
                        company_el = card.find("p", class_=re.compile(r"company", re.I)) or card.find("span", class_=re.compile(r"company", re.I))
                        link_el = card.find("a", href=True)
                        if title_el:
                            title = title_el.get_text(strip=True)
                            comp = company_el.get_text(strip=True) if company_el else "Entreprise HelloWork"
                            apply_url = "https://www.hellowork.com" + link_el["href"] if link_el and link_el["href"].startswith("/") else (link_el["href"] if link_el else url)
                            results.append(JobListing(
                                title=title,
                                company=comp,
                                location=location,
                                contract="CDI",
                                description=f"Offre d'emploi HelloWork : {title} chez {comp}.",
                                apply_url=apply_url,
                                platform="HelloWork"
                            ))
            else:
                logger.warning(f"[HelloWork] HTTP status {resp.status_code}")

        except Exception as e:
            logger.error(f"[HelloWork] Error: {e}")

        logger.info(f"✅ [HelloWork] Found {len(results)} listings.")
        self._sleep_rate_limit("HelloWork")
        return results

    # -------------------------------------------------------------------------
    # 4. France Travail (francetravail)
    # -------------------------------------------------------------------------
    def scrape_france_travail(self, query: str, location: str = "Paris", limit: int = 10) -> List[JobListing]:
        """
        Scrapes France Travail (formerly Pôle Emploi).
        Uses public web candidate search interface and structured search results.
        """
        logger.info(f"🔍 [France Travail] Scraping France Travail for '{query}' in '{location}'...")
        results: List[JobListing] = []

        if not self.session:
            return results

        try:
            encoded_query = quote_plus(query)
            encoded_loc = quote_plus(location)
            url = f"https://candidat.francetravail.fr/offres/recherche?motsCles={encoded_query}&lieux={encoded_loc}"

            headers = dict(COMMON_HEADERS)
            headers["Referer"] = "https://candidat.francetravail.fr"

            resp = self.session.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                html = resp.text
                if BeautifulSoup:
                    soup = BeautifulSoup(html, "html.parser")
                    items = soup.find_all("li", attrs={"data-id-offre": True}) or soup.find_all("li", class_=re.compile(r"result", re.I))

                    for item in items[:limit]:
                        offer_id = item.get("data-id-offre", "")
                        title_el = item.find("h2") or item.find("h3") or item.find("a")
                        comp_el = item.find("p", class_=re.compile(r"sub-title", re.I))
                        desc_el = item.find("p", class_=re.compile(r"description", re.I))

                        title = title_el.get_text(strip=True) if title_el else "Ingénieur / Développeur"
                        company = comp_el.get_text(strip=True) if comp_el else "France Travail Recruteur"
                        desc = desc_el.get_text(strip=True) if desc_el else f"Offre d'emploi France Travail : {title}"
                        apply_url = f"https://candidat.francetravail.fr/offres/recherche/detail/{offer_id}" if offer_id else url

                        results.append(JobListing(
                            title=title,
                            company=company,
                            location=location,
                            contract="CDI",
                            description=desc,
                            apply_url=apply_url,
                            platform="France Travail"
                        ))
            else:
                logger.warning(f"[France Travail] HTTP status {resp.status_code}")

        except Exception as e:
            logger.error(f"[France Travail] Error: {e}")

        logger.info(f"✅ [France Travail] Found {len(results)} listings.")
        self._sleep_rate_limit("France Travail")
        return results

    # -------------------------------------------------------------------------
    # 5. APEC (apec)
    # -------------------------------------------------------------------------
    def scrape_apec(self, query: str, location: str = "Paris", limit: int = 10) -> List[JobListing]:
        """
        Scrapes APEC (Association Pour l'Emploi des Cadres).
        Utilizes APEC's official public webservice search endpoint used by their SPA,
        completely avoiding HTML scraping & bot blocks.
        """
        logger.info(f"🔍 [APEC] Querying APEC public API for '{query}' in '{location}'...")
        results: List[JobListing] = []

        if not self.session:
            return results

        try:
            api_url = "https://www.apec.fr/cms/webservices/rechercheOffre"
            
            # Map location to APEC codes (e.g. 75 for Paris)
            loc_codes = ["75"] if "paris" in location.lower() else []

            payload = {
                "motsCles": query,
                "lieux": loc_codes,
                "pagination": {
                    "range": 0,
                    "taille": limit
                }
            }

            headers = {
                "User-Agent": COMMON_HEADERS["User-Agent"],
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.apec.fr",
                "Referer": "https://www.apec.fr/candidat/recherche-emploi.html/emploi"
            }

            resp = self.session.post(api_url, json=payload, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("resultats", []) or data.get("offres", [])
                for item in items[:limit]:
                    job_id = item.get("id") or item.get("numeroOffre")
                    title = item.get("intitule") or item.get("poste") or "Ingénieur Cadre"
                    company = item.get("nomCommercial") or item.get("enseigne") or "Entreprise Cadre APEC"
                    loc_text = item.get("lieu", {}).get("libelle") if isinstance(item.get("lieu"), dict) else (item.get("lieu") or location)
                    contract_type = item.get("typeContrat", "CDI - Statut Cadre")
                    desc = item.get("texteHtml") or item.get("description") or f"Offre Cadre APEC pour {title}."
                    # Clean html tags
                    clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()
                    apply_url = f"https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/{job_id}" if job_id else "https://www.apec.fr"

                    results.append(JobListing(
                        title=title,
                        company=company,
                        location=f"{loc_text} (France)",
                        contract=contract_type,
                        description=clean_desc[:500],
                        apply_url=apply_url,
                        platform="APEC (Cadres)"
                    ))
            else:
                logger.warning(f"[APEC] API status {resp.status_code}")

        except Exception as e:
            logger.error(f"[APEC] Error: {e}")

        logger.info(f"✅ [APEC] Found {len(results)} listings.")
        self._sleep_rate_limit("APEC")
        return results

    # -------------------------------------------------------------------------
    # Master Aggregator Function
    # -------------------------------------------------------------------------
    def scrape_all(
        self,
        query: str = "Senior Full Stack",
        location: str = "Paris",
        limit_per_portal: int = 5,
        strict_schema: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Executes multi-site search across all 5 French job portals:
          1. Welcome to the Jungle
          2. Indeed France
          3. HelloWork
          4. France Travail
          5. APEC

        Guarantees time.sleep(4) pacing to honor Gemini's 15 RPM limit.
        Returns a clean, standardized list of dictionaries containing:
          - title
          - company
          - location
          - contract
          - description
          - apply_url
        """
        all_jobs: List[JobListing] = []

        logger.info(f"🚀 Starting multi-site French job search for Xiao: '{query}' ({location})")
        logger.info("🛡️ Rate limiting active: 4.0s delay between portal requests (Gemini 15 RPM compliant)")

        # 1. Welcome to the Jungle
        try:
            all_jobs.extend(self.scrape_wttj(query, location, limit=limit_per_portal))
        except Exception as e:
            logger.error(f"Error scraping WTTJ: {e}")

        # 2. Indeed France
        try:
            all_jobs.extend(self.scrape_indeed(query, location, limit=limit_per_portal))
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")

        # 3. HelloWork
        try:
            all_jobs.extend(self.scrape_hellowork(query, location, limit=limit_per_portal))
        except Exception as e:
            logger.error(f"Error scraping HelloWork: {e}")

        # 4. France Travail
        try:
            all_jobs.extend(self.scrape_france_travail(query, location, limit=limit_per_portal))
        except Exception as e:
            logger.error(f"Error scraping France Travail: {e}")

        # 5. APEC
        try:
            all_jobs.extend(self.scrape_apec(query, location, limit=limit_per_portal))
        except Exception as e:
            logger.error(f"Error scraping APEC: {e}")

        logger.info(f"🎉 Aggregation complete: Scraped {len(all_jobs)} total listings across 5 French portals.")

        if strict_schema:
            return [job.to_clean_dict() for job in all_jobs]
        return [job.to_dict() for job in all_jobs]


def scrape_jobs(
    query: str = "Senior Full Stack",
    location: str = "Paris",
    limit_per_portal: int = 5,
    strict_schema: bool = True
) -> List[Dict[str, Any]]:
    """
    Convenience function returning the clean, standardized JSON list.
    """
    scraper = FrenchJobScraper(request_delay=4.0)
    return scraper.scrape_all(query=query, location=location, limit_per_portal=limit_per_portal, strict_schema=strict_schema)


if __name__ == "__main__":
    query_arg = sys.argv[1] if len(sys.argv) > 1 else "Full Stack Developer"
    loc_arg = sys.argv[2] if len(sys.argv) > 2 else "Paris"

    print(f"Executing multi-portal scrape for '{query_arg}' in '{loc_arg}'...")
    results = scrape_jobs(query=query_arg, location=loc_arg, limit_per_portal=3, strict_schema=True)

    print("\n--- STANDARDIZED JSON OUTPUT ---")
    print(json.dumps(results, indent=2, ensure_ascii=False))

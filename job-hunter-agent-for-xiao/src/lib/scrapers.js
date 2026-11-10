/**
 * Multi-Platform Job Fetcher & Normalizer
 * Interfaces with Welcome to the Jungle, APEC, LinkedIn, Indeed France, and France Travail.
 */

export interface ScraperSource {
  id: string;
  name: string;
  baseUrl: string;
  authRequired: boolean;
  searchUrlTemplate: string;
}

export const JOB_SOURCES: Record<string, ScraperSource> = {
  wttj: {
    id: 'wttj',
    name: 'Welcome to the Jungle',
    baseUrl: 'https://www.welcometothejungle.com',
    authRequired: false,
    searchUrlTemplate: 'https://www.welcometothejungle.com/fr/jobs?query={query}&aroundQuery={location}&contract_type=full_time'
  },
  apec: {
    id: 'apec',
    name: 'APEC (Cadres)',
    baseUrl: 'https://www.apec.fr',
    authRequired: false,
    searchUrlTemplate: 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={query}&lieux={location}'
  },
  linkedin: {
    id: 'linkedin',
    name: 'LinkedIn Jobs',
    baseUrl: 'https://www.linkedin.com/jobs',
    authRequired: false,
    searchUrlTemplate: 'https://www.linkedin.com/jobs/search/?keywords={query}&location={location}'
  },
  indeed: {
    id: 'indeed',
    name: 'Indeed France',
    baseUrl: 'https://fr.indeed.com',
    authRequired: false,
    searchUrlTemplate: 'https://fr.indeed.com/jobs?q={query}&l={location}'
  },
  francetravail: {
    id: 'francetravail',
    name: 'France Travail Tech',
    baseUrl: 'https://candidat.francetravail.fr',
    authRequired: false,
    searchUrlTemplate: 'https://candidat.francetravail.fr/offres/recherche?motsCles={query}&lieux={location}'
  }
};

/**
 * Builds normalized search queries across all 5 job boards.
 */
export function buildSearchQueries(role: string, location: string = 'Paris') {
  const encRole = encodeURIComponent(role);
  const encLoc = encodeURIComponent(location);

  return Object.values(JOB_SOURCES).map(source => ({
    sourceId: source.id,
    sourceName: source.name,
    targetUrl: source.searchUrlTemplate.replace('{query}', encRole).replace('{location}', encLoc)
  }));
}

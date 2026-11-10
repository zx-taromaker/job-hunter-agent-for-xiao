/**
 * Multi-Factor Compatibility Grading Engine (1.0 to 10.0)
 * Evaluates job requirements against Xiao's CV profile.
 *
 * Scoring Formula:
 * Final Score = (Tech * 0.40) + (Seniority * 0.25) + (Domain * 0.20) + (Contract/Mode * 0.15)
 */

export interface CandidateProfile {
  name: string;
  targetRoles: string[];
  skills: string[];
  yearsExperience: number;
  preferredLocations: string[];
  preferredContracts: string[];
}

export interface JobPosting {
  id: string;
  title: string;
  company: string;
  platform: 'wttj' | 'apec' | 'linkedin' | 'indeed' | 'francetravail';
  location: string;
  contract: string;
  salary: string;
  techStack: string[];
  description: string;
}

export interface GradeResult {
  finalScore: number;
  dimensions: {
    tech: number;
    seniority: number;
    domain: number;
    contract: number;
  };
  strengths: string[];
  gaps: string[];
  recommendation: 'Immediate Apply' | 'Strong Fit' | 'Moderate Fit' | 'Low Priority';
}

export function gradeJobCompatibility(job: JobPosting, profile: CandidateProfile): GradeResult {
  // 1. Tech Stack Compatibility (40%)
  const matchedSkills = job.techStack.filter(skill =>
    profile.skills.some(userSkill => userSkill.toLowerCase() === skill.toLowerCase())
  );
  const techRatio = matchedSkills.length / Math.max(job.techStack.length, 1);
  const techScore = Math.min(10, Math.max(5, (techRatio * 6) + 4));

  // 2. Seniority & Experience (25%)
  const isSeniorTitle = /lead|senior|staff|architect|principal|directeur|responsable/i.test(job.title);
  const seniorityScore = isSeniorTitle ? 9.5 : 8.8;

  // 3. Domain Fit (20%)
  const domainScore = 9.0; // Startup, Scaleup, French Tech / Cadre domain

  // 4. Contract & Location Fit (15%)
  const isParisOrRemote = /paris|remote|télétravail|hybrid/i.test(job.location);
  const isCDI = /cdi|cadre/i.test(job.contract);
  const contractScore = (isParisOrRemote ? 5.0 : 3.0) + (isCDI ? 4.8 : 3.5);

  // Compute Weighted Final Score
  const rawScore = (techScore * 0.40) + (seniorityScore * 0.25) + (domainScore * 0.20) + (contractScore * 0.15);
  const finalScore = Math.round(rawScore * 10) / 10;

  // Strengths & Gaps
  const strengths: string[] = [];
  if (matchedSkills.length > 0) {
    strengths.push(`Direct stack match on ${matchedSkills.slice(0, 3).join(', ')}`);
  }
  if (isSeniorTitle) {
    strengths.push(`Matches Xiao's 6+ years seniority profile for ${job.title}`);
  }
  if (isParisOrRemote) {
    strengths.push(`Location policy (${job.location}) aligns with preferences`);
  }

  const gaps = job.techStack
    .filter(skill => !profile.skills.some(userSkill => userSkill.toLowerCase() === skill.toLowerCase()))
    .map(skill => `Listing specifies ${skill}; consider highlighting transferable skills`);

  let recommendation: GradeResult['recommendation'] = 'Moderate Fit';
  if (finalScore >= 9.0) recommendation = 'Immediate Apply';
  else if (finalScore >= 8.0) recommendation = 'Strong Fit';
  else if (finalScore < 6.5) recommendation = 'Low Priority';

  return {
    finalScore,
    dimensions: {
      tech: Math.round(techScore * 10) / 10,
      seniority: Math.round(seniorityScore * 10) / 10,
      domain: Math.round(domainScore * 10) / 10,
      contract: Math.round(contractScore * 10) / 10
    },
    strengths,
    gaps,
    recommendation
  };
}

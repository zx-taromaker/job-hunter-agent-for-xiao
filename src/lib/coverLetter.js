/**
 * Cover Letter Synthesis & CV Tailoring Suggestions Engine
 * Produces personalized application text for Xiao in French and English.
 */

export interface LetterOptions {
  tone: 'startup' | 'executive' | 'technical';
  language: 'fr' | 'en';
  candidateName: string;
  candidateEmail: string;
}

export function generateCoverLetter(job: any, options: LetterOptions): string {
  const { tone, language, candidateName, candidateEmail } = options;

  if (language === 'fr') {
    if (tone === 'startup') {
      return `Madame, Monsieur,\n\nC'est avec un vif enthousiasme que je vous adresse ma candidature pour le poste de ${job.title} au sein de ${job.company}.\n\nAvec plus de 6 ans d'expérience dans la conception d'architectures web robustes et scalables (${job.techStack.slice(0, 3).join(', ')}), je suis de près les réalisations de votre équipe.\n\nCe que j'apporte concrètement à votre équipe :\n- Une solide maîtrise de l'écosystème ${job.techStack[0]} et ${job.techStack[1]}, garantissant des applications fiables et maintenables.\n- Une expérience éprouvée dans l'optimisation des performances applicatives et la résilience des APIs.\n- Une sensibilité produit affirmée, favorisant l'impact utilisateur et une collaboration fluide avec le design et le product management.\n\nJe serais ravi de vous rencontrer lors d'un entretien pour échanger sur vos priorités techniques et la façon dont je peux contribuer aux défis de ${job.company}.\n\nBien cordialement,\n\n${candidateName}\n${candidateEmail} | Paris, France`;
    }
    if (tone === 'executive') {
      return `À l'attention de la Direction du Recrutement,\n\nObjet : Candidature au poste de ${job.title}\n\nMadame, Monsieur,\n\nJe vous adresse par la présente ma candidature pour la fonction de ${job.title} au sein de votre entreprise ${job.company}.\n\nFort d'un parcours d'ingénieur confirmé marqué par la direction technique de projets critiques, je mets au service de vos ambitions mon expertise approfondie en architectures logicielles distribuées (${job.techStack.join(', ')}).\n\nMon profil combine rigueur d'ingénierie logicielle, anticipation des contraintes de sécurité et capacité à fédérer des équipes vers l'excellence opérationnelle.\n\nDans l'attente d'une opportunité d'échange, je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.\n\n${candidateName}\nIngénieur Cadre | Paris`;
    }
    return `Hello l'équipe ${job.company},\n\nJe postule avec grand intérêt au rôle de ${job.title}.\n\nAlignement technique direct avec votre stack :\n• ${job.techStack.slice(0, 2).join(' & ')} : Composants découplés, gestion d'état optimisée et couverture de tests rigoureuse.\n• Backend & Cloud (${job.techStack.slice(2).join(', ')}) : Pipelines CI/CD, conteneurisation Docker et APIs ultra-résilientes.\n\nPrêt à délivrer avec autonomie dès le premier sprint.\n\nBest,\n${candidateName}`;
  }

  // English fallback
  return `Dear Hiring Team at ${job.company},\n\nI am thrilled to submit my application for the ${job.title} position.\n\nWith over 6 years of experience engineering high-scale web platforms using ${job.techStack.slice(0, 4).join(', ')}, I am excited by the opportunity to contribute to ${job.company}'s engineering initiatives.\n\nI look forward to discussing how my background aligns with your team's goals.\n\nWarm regards,\n\n${candidateName}\n${candidateEmail} | Paris, France`;
}

export function generateCVSuggestions(job: any): string[] {
  return [
    `Highlight your concrete achievements with ${job.techStack[0]} and ${job.techStack[1]} at the very top of your experience section.`,
    `Quantify latency improvements or system scale handled (e.g. 'handled 10k+ daily active users with 99.9% uptime').`,
    `Mention collaborative experience with cross-functional product and design teams in fast-paced environments.`
  ];
}

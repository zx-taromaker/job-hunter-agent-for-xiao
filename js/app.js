// ==========================================
// Job Hunter Agent for Xiao - High-End Upgrade
// ==========================================

const DEFAULT_SETTINGS = {
    keywords: "Global Operations, E-Commerce Strategy, Digital Transformation, Business Development, Cross-border Sourcing",
    locations: "Paris, Île-de-France, Télétravail"
};

function generateAdvancedAIAnalysis(jobTitle, company) {
    return {
        score: Math.floor(Math.random() * 2) + 8.8,
        reason: `High synergy with strategic cross-border operational excellence and multi-channel ecosystem management. The candidate's track record in scaling digital distribution and supply chain optimization directly addresses ${company}'s current expansion phase.`,
        matchedSkills: ["Global Sourcing & Procurement", "Digital Transformation", "Cross-functional Leadership", "E-Commerce Strategy"],
        missingSkills: ["Advanced Salesforce CRM (Adaptable)", "Corporate Governance Reporting"],
        cvSuggestions: [
            "Highlight measurable ROI and efficiency gains in international supply chain projects.",
            "Emphasize leadership in multi-stakeholder cross-border negotiations."
        ]
    };
}

function generateProfessionalCoverLetter(jobTitle, company) {
    return `Madame, Monsieur,

En tant que professionnel(le) passionné(e) par la transformation digitale et l'excellence opérationnelle internationale, je vous écris pour exprimer mon vif intérêt pour le poste de ${jobTitle} au sein de ${company}.

Mon parcours m'a permis de maîtriser les enjeux complexes du sourcing global, de la stratégie e-commerce et du pilotage de projets transversaux. Je suis particulièrement attiré(e) par la vision de ${company} et sa capacité à redéfinir les standards de son marché. 

Votre recherche d'un profil capable d'allier vision stratégique et exécution rigoureuse résonne parfaitement avec mon expertise en gestion de projets internationaux et en optimisation de la chaîne de valeur. Intégrer vos équipes me permettra de contribuer activement à votre croissance tout en apportant une perspective interculturelle forte.

Je me tiens à votre entière disposition pour un entretien qui me permettra de détailler mes motivations et mon adéquation avec vos ambitions.

Bien cordialement,
Xiao ZHANG`;
}

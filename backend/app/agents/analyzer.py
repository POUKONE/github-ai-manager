from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class AnalyzerAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.2)

    def generate_action_plan(self, metrics: dict) -> str:
        """Demande à l'IA d'analyser les métriques et de concevoir une roadmap de correctifs."""
        
        # SÉCURITÉ ABSOLUE : On extrait les données sous forme de texte brut SANS ACCLODES (Exit le JSON brut)
        if metrics['complex_functions']:
            complex_txt = ""
            for func in metrics['complex_functions']:
                complex_txt += f"- Fichier : {func['file']}, Fonction : {func['entity']} (Complexité : {func['complexity']}, Rang : {func['rank']})\n"
        else:
            complex_txt = "Aucune fonction complexe détectée."

        if metrics['low_maintainability_files']:
            maintainability_txt = ""
            for file_info in metrics['low_maintainability_files']:
                maintainability_txt += f"- Fichier : {file_info['file']} (Score de maintenabilité : {file_info['score']}/100)\n"
        else:
            maintainability_txt = "Aucun fichier à faible maintenabilité."
        
        system_prompt = (
            "Tu es un Architecte Logiciel Senior et un Tech Lead d'élite.\n"
            "On te fournit un rapport technique brut des métriques d'un dépôt de code.\n"
            "Ton travail est de rédiger un plan d'action de maintenance priorisé et ultra-professionnel.\n"
            "Sois concis, pragmatique et oriente tes réponses vers la création de valeur (Clean Code, Tests, Doc).\n"
            "Réponds en Markdown clair."
        )
        
        user_prompt = (
            "Voici les métriques récoltées sur le dépôt :\n"
            "----------------------------------------\n"
            f"Fichiers Python détectés : {metrics['total_files']}\n"
            f"Absence de README.md : {metrics['missing_readme']}\n"
            f"Fonctions trop complexes détectées :\n{complex_txt}\n"
            f"Fichiers à faible maintenabilité :\n{maintainability_txt}\n"
            "----------------------------------------\n\n"
            "Génère un plan d'action basé exclusivement sur ces données. Priorise sous forme de tâches (ex: Priorité Haute, Moyenne, Basse)."
        )
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        
        chain = prompt_template | self.llm
        response = chain.invoke({})
        return response.content
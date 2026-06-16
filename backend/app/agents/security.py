from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class SecurityAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.0)

    def analyze_vulnerabilities(self, bandit_report: str) -> str:
        """Analyse le rapport Bandit et génère des consignes de correction strictes."""
        system_prompt = (
            "Tu es un Expert en Cybersécurité (SecOps) spécialisé en Python.\n"
            "Ton rôle est d'analyser les rapports de l'outil Bandit et d'expliquer comment corriger les failles.\n"
            "Sois concis, direct et donne des consignes strictes au développeur."
        )
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Voici le rapport d'erreur de l'outil Bandit :\n{{bandit_report}}\n\nRédige les instructions de correction.")
        ], template_format="mustache")
        
        chain = prompt_template | self.llm
        response = chain.invoke({"bandit_report": bandit_report})
        return response.content.strip()
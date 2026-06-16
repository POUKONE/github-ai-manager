from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CoderAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.1)

    def generate_tests(self, file_name: str, file_content: str, rules: str = "") -> str:
        """Génère un fichier de test pytest complet en respectant la base de connaissances (RAG)."""
        
        system_prompt = (
            "Tu es un Développeur Python Senior expert en Tests Unitaires.\n"
            "Ton but est d'écrire un fichier de test utilisant `pytest` pour le code fourni.\n"
            "Tu dois STRICTEMENT respecter les règles de codage de l'entreprise fournies ci-dessous.\n\n"
            "--- RÈGLES DE CODAGE À RESPECTER ---\n"
            f"{rules}\n"
            "------------------------------------\n\n"
            "Renvoie UNIQUEMENT le code Python valide, sans bloc Markdown (pas de ```python)."
        )
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Voici le contenu du fichier {{file_name}} :\n----------------------------------------\n{{file_content}}\n----------------------------------------\n\nGénère le fichier de test.")
        ], template_format="mustache")
        
        chain = prompt_template | self.llm
        response = chain.invoke({
            "file_name": file_name,
            "file_content": file_content
        })
        return response.content.strip()
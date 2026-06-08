from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CoderAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.1)

    def generate_tests(self, file_name: str, file_content: str) -> str:
        """Génère un fichier de test pytest complet pour le code fourni."""
        
        system_prompt = (
            "Tu es un Développeur Python Senior expert en Tests Unitaires.\n"
            "Ton but est d'écrire un fichier de test utilisant `pytest` pour le code qui te sera fourni.\n"
            "Renvoie UNIQUEMENT le code Python valide. Ne mets AUCUN commentaire d'explication, "
            "AUCUN texte avant ou après, et n'utilise PAS de blocs de code Markdown (pas de ```python)."
        )
        
        # En passant template_format="mustache", LangChain n'analysera plus les accolades simples {} comme des variables.
        # Les variables LangChain devront être déclarées avec des doubles accolades {{ variable }}
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Voici le contenu du fichier {{file_name}} :\n----------------------------------------\n{{file_content}}\n----------------------------------------\n\nGénère un fichier de test robuste couvrant les différents cas possibles (edge cases).")
        ], template_format="mustache")
        
        # On injecte les variables de manière sécurisée
        chain = prompt_template | self.llm
        response = chain.invoke({
            "file_name": file_name,
            "file_content": file_content
        })
        return response.content.strip()
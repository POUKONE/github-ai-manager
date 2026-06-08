import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate

# Configuration du PATH
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.github_client import GitHubClientManager
from app.core.analyzer_tools import CodeStaticAnalyzer
from app.agents.analyzer import AnalyzerAgent
from app.agents.coder import CoderAgent
from app.core.guardrails import CodeGuardrails

load_dotenv()

def main():
    token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not token or not openai_key:
        raise ValueError("Clés manquantes dans le fichier .env")

    # Initialisation de notre équipe d'agents
    gh_manager = GitHubClientManager(token)
    analyzer_agent = AnalyzerAgent(openai_key)
    coder_agent = CoderAgent(openai_key)
    
    TARGET_REPO = "POUKONE/sandbox-ai" 
    AI_BRANCH = f"ai/feature-tests-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    print(f"--- Démarrage de la Pipeline Intelligente sur {TARGET_REPO} ---")
    
    try:
        # 1. Isolation & Clonage
        local_path = gh_manager.clone_and_branch(TARGET_REPO, AI_BRANCH)
        
        # 2. Analyse (Data Extraction)
        metrics = CodeStaticAnalyzer.analyze_directory(local_path)
        print(f"Analyse terminée. Fichiers complexes trouvés : {len(metrics['complex_functions'])}")
        
        # 3. Stratégie de l'Agent Coder si un fichier nécessite des tests
        if metrics['complex_functions']:
            target_file_info = metrics['complex_functions'][0] # On prend le premier fichier complexe
            target_file_name = target_file_info['file']
            target_file_path = os.path.join(local_path, target_file_name)
            
            with open(target_file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            
            print(f"L'Agent Coder génère les tests pour {target_file_name}...")
            generated_test_code = coder_agent.generate_tests(target_file_name, source_code)
            
            # Écriture du fichier de test en local (ex: test_calculateur.py)
            test_file_name = f"test_{target_file_name}"
            test_file_path = os.path.join(local_path, test_file_name)
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(generated_test_code)
            
            # 4. Étape de Guardrail (Validation) avec boucle d'auto-correction
            max_retries = 3
            retry_count = 0
            success = False
            report = ""

            while retry_count < max_retries:
                # ---> AJOUT DE LOGS POUR LE PORTFOLIO <---
                if os.path.exists(test_file_path):
                    with open(test_file_path, "r", encoding="utf-8") as f:
                        current_code = f.read()
                    print(f"\n--- [LOG] Code testé à la tentative {retry_count + 1} : ---\n{current_code}\n---------------------------------------------\n")
                
                success, report = CodeGuardrails.verify_tests(local_path)
                
                if success:
                    print(f"✅ Guardrails Validés à la tentative {retry_count + 1} ! Le code est sain.")
                    break
                else:
                    retry_count += 1
                    if retry_count >= max_retries:
                        break
                        
                    print(f"⚠️ Tentative {retry_count} échouée. L'Agent Coder tente de corriger son code...")
                    
                    system_prompt_correction = (
                        "Tu es un Développeur Python Senior. Les tests que tu as générés ont échoué.\n"
                        "Analyse le rapport d'erreur de pytest et réécris le fichier de test pour qu'il passe à 100%.\n"
                        "Renvoie UNIQUEMENT du code Python valide, sans bloc Markdown, sans commentaires."
                    )
                    
                    user_prompt_correction = (
                        "Voici le code source original :\n{{source_code}}\n\n"
                        "Voici le rapport d'erreur de pytest :\n{{report}}\n\n"
                        "Réécris et corrige le fichier de test complet."
                    )
                    
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", system_prompt_correction),
                        ("user", user_prompt_correction)
                    ], template_format="mustache")
                    
                    chain = prompt_template | coder_agent.llm
                    corrected_code = chain.invoke({
                        "source_code": source_code,
                        "report": report
                    }).content.strip()
                    
                    with open(test_file_path, "w", encoding="utf-8") as f:
                        f.write(corrected_code)

            # 5. Décision finale après les tentatives
            if success:
                gh_manager.commit_and_push(local_path, f"test(ai): ajout des tests automatiques pour {target_file_name}", AI_BRANCH)
                
                pr_url = gh_manager.create_pull_request(
                    repo_full_name=TARGET_REPO,
                    title=f"test(ai): couverture de tests validée pour {target_file_name}",
                    body=f"Bonjour !\n\nL'**Agent Coder** a généré et corrigé de manière autonome une suite de tests unitaires passants pour `{target_file_name}`.\n\n**Rapport final des Guardrails :**\n```txt\n{report}\n```",
                    head_branch=AI_BRANCH,
                    base_branch="main"
                )
                print(f"Pipeline réussie avec auto-correction ! PR : {pr_url}")
            else:
                print(f"❌ Échec persistant après {max_retries} tentatives. Abandon de la PR pour sécurité.")

    except Exception as e:
        print(f"Une erreur est survenue lors de l'exécution : {e}")

if __name__ == "__main__":
    main()
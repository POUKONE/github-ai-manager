import subprocess
import os

class CodeGuardrails:
    @staticmethod
    def verify_tests(repo_path: str) -> tuple[bool, str]:
        """Exécute pytest sur le dépôt temporaire et capture le résultat."""
        print("Guardrails : Exécution de pytest pour valider les modifications...")
        
        try:
            # On lance pytest en ciblant le dossier temporaire
            result = subprocess.run(
                ["pytest", repo_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Tous les tests passent avec succès !"
            else:
                # On combine stdout et stderr pour donner le maximum de contexte à l'IA en cas d'échec
                error_log = result.stdout + "\n" + result.stderr
                return False, error_log
                
        except Exception as e:
            return False, f"Erreur critique lors de l'exécution de pytest : {str(e)}"
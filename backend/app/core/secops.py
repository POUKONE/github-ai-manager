import subprocess
import os

class SecurityGuard:
    @staticmethod
    def audit_code_safety(file_path: str) -> tuple[bool, str]:
        """
        Exécute un scan de sécurité Bandit sur un fichier Python spécifique.
        Ignore la règle B101 (assert) uniquement si c'est un fichier de test.
        """
        file_name = os.path.basename(file_path)
        print(f"SecOps : Analyse de sécurité sur {file_name}...")
        
        # Commande de base pour lancer Bandit de manière silencieuse
        command = ["bandit", "-q"]
        
        # CORRECTION DU FLAG : "-s" au lieu de "-sk" pour ignorer proprement B101
        if file_name.startswith("test_"):
            command.extend(["-s", "B101"])
            
        command.append(file_path)
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            
            # Bandit renvoie 0 si aucune vulnérabilité n'est trouvée (ou si elles sont ignorées)
            if result.returncode == 0:
                return True, "Aucune faille de sécurité légitime détectée dans le code généré."
            else:
                return False, f"VULNÉRABILITÉS DÉTECTÉES :\n{result.stdout}\n{result.stderr}"
                
        except Exception as e:
            return False, f"Erreur lors du scan SecOps : {str(e)}"
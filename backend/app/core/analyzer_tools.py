import os
from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit

class CodeStaticAnalyzer:
    """Outil d'analyse statique pour extraire des métriques concrètes du code."""
    
    @staticmethod
    def analyze_directory(directory_path: str) -> dict:
        report = {
            "total_files": 0,
            "complex_functions": [],
            "low_maintainability_files": [],
            "missing_readme": not os.path.exists(os.path.join(directory_path, "README.md"))
        }
        
        for root, _, files in os.walk(directory_path):
            # On ignore les dossiers virtuels et Git
            if any(part in root for part in [".git", "venv", "__pycache__", ".env"]):
                continue
                
            for file in files:
                if file.endswith(".py"):
                    report["total_files"] += 1
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    
                    # 1. Analyse de la complexité cyclomatique (Score de A à F)
                    try:
                        blocks = cc_visit(code)
                        for block in blocks:
                            # Si la complexité est élevée (Rank C ou pire, ou score > 5)
                            if block.complexity > 5:
                                report["complex_functions"].append({
                                    "file": os.path.relpath(file_path, directory_path),
                                    "entity": block.name,
                                    "complexity": block.complexity,
                                    "rank": cc_rank(block.complexity)
                                })
                    except Exception:
                        pass # Fichier syntaxiquement incorrect ignoré pour le test
                        
                    # 2. Indice de maintenabilité (Score de 0 à 100)
                    try:
                        mi_score = mi_visit(code, multi=True)
                        if mi_score < 70:  # En dessous de 70, le code devient difficile à maintenir
                            report["low_maintainability_files"].append({
                                "file": os.path.relpath(file_path, directory_path),
                                "score": round(mi_score, 2)
                            })
                    except Exception:
                        pass
                        
        return report
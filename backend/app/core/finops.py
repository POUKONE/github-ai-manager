import tiktoken

class TokenGuard:
    def __init__(self, model_name: str = "gpt-4o-mini", max_allowed_tokens: int = 2000):
        self.model_name = model_name
        self.max_allowed_tokens = max_allowed_tokens
        try:
            # Récupère l'encodage spécifique au modèle OpenAI choisi
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Encodage de secours par défaut si le modèle est trop récent
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def verify_budget(self, text: str) -> tuple[bool, int, str]:
        """
        Calcule les tokens et valide si cela rentre dans le budget FinOps.
        Retourne : (Est-ce que ça passe ?, Nombre de tokens, Message d'analyse)
        """
        token_count = len(self.encoding.encode(text))
        
        if token_count > self.max_allowed_tokens:
            msg = f"❌ [FinOps Alert] Le fichier contient {token_count} tokens. La limite stricte est fixée à {self.max_allowed_tokens} tokens."
            return False, token_count, msg
            
        msg = f"💰 [FinOps] Fichier validé : {token_count} tokens estimés pour {self.model_name}."
        return True, token_count, msg
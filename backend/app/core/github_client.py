import os
import tempfile
from github import Github
from git import Repo

class GitHubClientManager:
    def __init__(self, token: str):
        self.gh = Github(token)
        self.token = token
        # Dossier temporaire isolé pour les manipulations de code
        self.temp_dir = tempfile.mkdtemp(prefix="gh_ai_mgr_")

    def get_user_repositories(self):
        """Récupère tous les dépôts publics et privés de l'utilisateur."""
        user = self.gh.get_user()
        return [repo.full_name for repo in user.get_repos()]

    def clone_and_branch(self, repo_full_name: str, branch_name: str) -> str:
        """Clone un dépôt à distance dans un dossier temporaire et crée une nouvelle branche."""
        repo_url = f"https://x-access-token:{self.token}@github.com/{repo_full_name}.git"
        local_path = os.path.join(self.temp_dir, repo_full_name.split('/')[-1])
        
        print(f"Clonage de {repo_full_name} vers {local_path}...")
        local_repo = Repo.clone_from(repo_url, local_path)
        
        # Création et bascule sur la nouvelle branche pour l'IA
        new_branch = local_repo.create_head(branch_name)
        new_branch.checkout()
        
        return local_path

    def commit_and_push(self, repo_path: str, commit_message: str, branch_name: str):
        """Commit tous les changements locaux et push la branche vers le serveur distant."""
        local_repo = Repo(repo_path)
        local_repo.git.add(A=True)  # Ajoute tous les fichiers modifiés/créés
        local_repo.index.commit(commit_message)
        
        print(f"Push de la branche {branch_name} vers GitHub...")
        origin = local_repo.remote(name='origin')
        origin.push(branch_name)

    def create_pull_request(self, repo_full_name: str, title: str, body: str, head_branch: str, base_branch: str = "main"):
        """Ouvre une véritable Pull Request sur GitHub."""
        repo = self.gh.get_repo(repo_full_name)
        pr = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
        print(f"Pull Request créée avec succès : {pr.html_url}")
        return pr.html_url
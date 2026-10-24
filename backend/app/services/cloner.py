import os
import tempfile
from git import Repo
from pathlib import Path

class RepoCloner:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    def clone_and_scan(self):
        # Create a temporary directory that auto-deletes when done
        temp_dir = tempfile.TemporaryDirectory()
        try:
            # Clone the repository into the temporary directory
            Repo.clone_from(self.repo_url, temp_dir.name)
            
            # Scan all files using pathlib
            repo_path = Path(temp_dir.name)
            files = []
            
            for path in repo_path.glob("**/*"):
                # Skip hidden git files and directories
                if ".git" in path.parts:
                    continue
                if path.is_file():
                    # Get relative path from repo root
                    relative_path = path.relative_to(repo_path)
                    files.append(str(relative_path))
                    
            return files
        finally:
        # Clean up temporary directory
            temp_dir.cleanup()
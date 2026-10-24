import tempfile
from pathlib import Path
import git
from fastapi import HTTPException
from app.config import settings

class RepoCloner:
    @staticmethod
    def clone_repository(repo_url: str) -> tuple[tempfile.TemporaryDirectory, Path]:
        """
        Clones a GitHub repository into a secure temporary directory.
        Returns the temp_dir object (to keep it alive) and the Path object to the repo.
        """
        temp_dir = tempfile.TemporaryDirectory()
        repo_path = Path(temp_dir.name)

        try:
           
            git.Repo.clone_from(
                url=str(repo_url),
                to_path=repo_path,
                depth=1,
                single_branch=True
            )
        except git.GitCommandError as e:
            temp_dir.cleanup()
            raise HTTPException(
                status_code=400,
                detail=f"Git clone failed. Check if the repository URL is valid and public. Error: {e.stderr.strip()}"
            )
        except Exception as e:
            temp_dir.cleanup()
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred during repository cloning: {str(e)}"
            )

        return temp_dir, repo_path
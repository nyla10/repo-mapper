from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.cloner import RepoCloner

router = APIRouter(prefix="/repo", tags=["Repository"])

class CloneRequest(BaseModel):
    repo_url: str

@router.post("/clone")
def clone_repository(request: CloneRequest):
    try:
        cloner = RepoCloner(request.repo_url)
        files = cloner.clone_and_scan()
        return {
            "message": "Repository cloned and scanned successfully!",
            "total_files": len(files),
            "files": files[:50]  # Return first 50 files as a preview
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
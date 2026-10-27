
import base64
import os
import re
from urllib.parse import quote

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.analyzer import analyze_files

router = APIRouter()


class AnalyzeRequest(BaseModel):
    url: str


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/analyze")
def analyze_repository(request: AnalyzeRequest):
    pattern = (
        r"^https?://github\.com/"
        r"([A-Za-z0-9_.-]+)/"
        r"([A-Za-z0-9_.-]+)/?$"
    )

    match = re.match(pattern, request.url.strip())

    if not match:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid GitHub repository URL.",
        )

    owner, repo = match.groups()

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "RepoMapper",
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_url = (
        f"https://api.github.com/repos/{owner}/{repo}"
        "/git/trees/HEAD?recursive=1"
    )

    try:
        response = requests.get(
            api_url,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to GitHub.",
        ) from exc

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Repository not found or not publicly accessible.",
        )

    if response.status_code == 403:
        raise HTTPException(
            status_code=429,
            detail="GitHub rate limit or access restriction. Try again later.",
        )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail=f"GitHub returned status {response.status_code}.",
        )

    tree = response.json().get("tree", [])

    if response.json().get("truncated", False):
        raise HTTPException(
            status_code=422,
            detail="Repository tree is too large for complete analysis.",
        )

    allowed_extensions = (".js", ".jsx", ".ts", ".tsx")

    source_files = [
        item for item in tree
        if item.get("type") == "blob"
        and item.get("path", "").endswith(allowed_extensions)
        and item.get("size", 0) <= 200_000
    ]

    if len(source_files) > 500:
        raise HTTPException(
            status_code=413,
            detail="Repository has more than 500 supported source files.",
        )

    files = {}

    for item in source_files:
        path = item["path"]
        encoded_path = quote(path, safe="/")

        try:
            file_response = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}"
                f"/contents/{encoded_path}",
                headers=headers,
                timeout=15,
            )
        except requests.RequestException:
            continue

        if not file_response.ok:
            continue

        try:
            content = base64.b64decode(
                file_response.json()["content"]
            ).decode("utf-8", errors="replace")
        except (KeyError, ValueError):
            continue

        files[path] = content

    if not files:
        raise HTTPException(
            status_code=422,
            detail="No supported source files could be retrieved.",
        )

    result = analyze_files(files)

    return {
        "owner": owner,
        "repo": repo,
        "file_count": len(result["nodes"]),
        "dependency_count": len(result["edges"]),
        "nodes": result["nodes"],
        "edges": result["edges"],
    }

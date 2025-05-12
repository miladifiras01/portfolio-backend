from fastapi import APIRouter, HTTPException, Request
from app.database import engine
from app.models import Project
from sqlmodel import Session
import json
from app.services.project_service import *
import httpx
from config import settings
import base64
import markdown

github_router = APIRouter()
GITHUB_TOKEN = settings.GITHUB_TOKEN
GITHUB_API_URL = settings.GITHUB_API_URL


def handle_created(repository):
    try:
        project = get_project_by_column('github_url', repository.get("html_url"))
        if project:
            return handle_edited(repository)

        short_description = repository.get("description", "")
        description = repository.get("description", "") 
        repo_data = {
            "name": repository.get("name").replace("-", " ").title(),
            "short_description": short_description,
            "github_url": repository.get("html_url"),
        }
        owner = repository.get("owner", {}).get("login")
        repo_name = repository.get("name", "")
        url = repository.get('html_url', "")
        images = get_images(url, owner, repo_name)
        description = get_description(url, owner, repo_name)
        topics = repository.get("topics")
        repo_data["images"] = images
        repo_data["technologies"] = topics
        repo_data["description"] = description
        return create_project(**repo_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_edited(repository):
    try:
        project = get_project_by_column('github_url', repository.get("html_url"))
        short_description = repository.get("description", "")
        repo_data = {
            "name": repository.get("name").replace("-", " ").title(),
            "short_description": short_description,
            "github_url": repository.get("html_url"),
        }
        owner = repository.get("owner", {}).get("login")
        repo_name = repository.get("name", "")
        url = repository.get('html_url', "")
        images = get_images(url, owner, repo_name)
        topics = repository.get("topics")
        repo_data["images"] = images
        repo_data["technologies"] = topics
        update_project(project.id, **repo_data)
        return {"message": "Project updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_deleted(repository):
    try:
        project = get_project_by_column('github_url', repository.get("html_url"))
        delete_project(project.id)
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def handle_push(payload):
    try:
        repository = payload.get("repository", {})
        owner = repository.get("owner", {}).get("login")
        repo_name = repository.get("name")
        project = get_project_by_column("github_url", repository.get("html_url"))

        if not project:
            handle_created(repository)
        commits = payload.get("commits", [])
        modified_files = []
        for commit in commits:
            modified_files.extend(commit.get("added", []))
            modified_files.extend(commit.get("modified", []))
            modified_files.extend(commit.get("removed", []))
        image_changes = [
            file for file in modified_files if file.startswith("docs/images/")]
        description_change = any(file == "docs/description.md" for file in modified_files)
        repo_name = repository.get("name", "")
        url = repository.get('html_url', "")
        if not image_changes and not description_change:
            return {"message": "No changes detected in docs/images folder or docs/description. Skipping update."}
        if image_changes:
            images = get_images(url, owner, repo_name)
            update_images(project.id, images)

        if description_change:
            description = get_description(url, owner, repo_name)
            update_project(project.id, description=description)
            return {"message": "Project updated successfully.", "description": description}
        return {"message": "Project updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_images(url, owner, repo_name):
    try:
        api_url = f"{GITHUB_API_URL}/{owner}/{repo_name}/contents/docs/images"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/json"
        }
        with httpx.Client() as client:
            response = client.get(api_url, headers=headers)
            response.raise_for_status()
            files = response.json()

        image_urls = [
            file["download_url"] for file in files
            if file["name"].lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"))
        ]
        return image_urls

    except httpx.HTTPStatusError as e:
        print(f"Error fetching images: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_description(url, owner, repo_name):
    try:
        api_url = f"{GITHUB_API_URL}/{owner}/{repo_name}/contents/docs/description.md"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/json"
        }
        with httpx.Client() as client:
            response = client.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        content_base64 = data.get("content", "")
        content_decoded = base64.b64decode(content_base64).decode("utf-8")

        description_html = markdown.markdown(content_decoded)
        return description_html

    except httpx.HTTPStatusError as e:
        print(f"Error fetching description: {e}")
        return None
    except KeyError:
        print("Description file not found or missing content field.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
ACTION_HANDLERS = {
    "edited": handle_edited,
    "deleted": handle_deleted
}

@github_router.post("/webhook")
async def github_webhook(request: Request):
    try:
        payload = await request.json()
        event = request.headers.get("x-github-event", None)
        repository = payload.get("repository", {})
        if event == "ping":
            return handle_created(repository)
        if event == "push":
            return handle_push(payload)
        if event == "repository":
            action = payload.get("action")
            return ACTION_HANDLERS[action](repository)
        if event == "meta":
            action = payload.get("action")
            if action == "deleted":
                return handle_deleted(repository)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

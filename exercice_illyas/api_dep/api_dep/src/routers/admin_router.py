from fastapi import APIRouter

admin_rooter = APIRouter()

@admin_rooter.get("/")
def get_admin_dashboard():
    return {"message": "Bienvenue sur le tableau de bord Admin"}

@admin_rooter.post("/settings")
def update_settings(settings: dict):
    return {"message": "Paramètres mis à jour", "settings": settings}

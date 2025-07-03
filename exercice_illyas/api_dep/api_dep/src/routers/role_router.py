from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.role import Role
from models.role import RoleCreate
from utils.conn import get_session



router_role = APIRouter()

@router_role.get("/")
def get_users(db = Depends(get_session)):
    users = db.query(Role).all()  # récupère tous les utilisateurs
    return users

@router_role.post("/")
def create_role(role: RoleCreate, db: Session = Depends(get_session)):
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router_role.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_session)):
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")

    db.delete(role)
    db.commit()
    return {"message": f"Rôle avec l'id {role_id} supprimé."}

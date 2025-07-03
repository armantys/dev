from fastapi import APIRouter, Depends, HTTPException, status
from utils.conn import get_session
from models.user import CreateUser
from db.user import User
router_user = APIRouter()

@router_user.get("/")
def get_users(db = Depends(get_session)):
    users = db.query(User).all()  # récupère tous les utilisateurs
    return users

@router_user.post("/")
def create_user(user: CreateUser, db = Depends(get_session)):
    try:
        #hash le MDP
        db_user = User(username=user.username, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@router_user.delete("/{user_id}")
def delete_role(user_id: int, db = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")

    db.delete(user)
    db.commit()
    return {"message": f"Utilisateur {user_id} supprimé."}


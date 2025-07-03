from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Field
from middlewares.process_time import add_process_time_header
from routers.user_router import router_user as user_router
from routers.admin_router import admin_rooter as admin_router
from routers.role_router import router_role as role_router
app = FastAPI()


# Middleware
app.middleware("http")(add_process_time_header)

# Inclure les routeurs
app.include_router(user_router, prefix="/user")
app.include_router(admin_router, prefix="/admin")
app.include_router(role_router, prefix="/role")

@app.on_event("startup")
def on_startup():
    postgres_url = "postgresql://ROOT:ROOT@localhost:5432/BDD_TEST"
    engine = create_engine(postgres_url)
    # Créer les tables dans la base si elles n'existent pas
    SQLModel.metadata.create_all(engine)
    print("tablecreate")

from fastapi import FastAPI
from database import Base, engine
from models import connection
from routers import connections

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkUp Connection Service")
app.include_router(connections.router)
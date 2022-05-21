import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db
from app.routes.auth import auth_router
from app.routes.comment_and_like import comment_and_like_router
from app.routes.follow import follow_router
from app.routes.post import post_router
from app.routes.user import user_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

asyncio.create_task(init_db())


@app.get(
    "/",
    tags=["Welcome"]
)
def welcome():
    return {"message": "Welcome to Ultesa Blockbuster API!"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(follow_router)
app.include_router(post_router)
app.include_router(comment_and_like_router)

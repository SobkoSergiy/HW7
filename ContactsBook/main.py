from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import uvicorn
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from services.config import settings 
from routes import auth, contacts, users


@asynccontextmanager
async def lifespan(app: FastAPI):   
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)
    yield

app = FastAPI(lifespan=lifespan)


origins = [ "http://localhost:3000", "http://localhost:5000" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/users')
app.include_router(contacts.router, prefix='/contacts')


@app.get("/", dependencies=[Depends(RateLimiter(times=1, seconds=7))])
def read_root():
    """
    Returns the root started message.

    :return: Root message.
    :rtype: dict
    """
    return {"(hw14) root message": "FastAPI started!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


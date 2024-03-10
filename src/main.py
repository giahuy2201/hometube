from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import signal

from core.database import Base, engine
from daemon.service import stop_daemon, start_daemon
import daemon.router as daemon
import channels.router as channels
import medias.router as medias
import presets.router as presets


@asynccontextmanager
async def lifespan(app: FastAPI):
    # run daemon on startup
    start_daemon()
    yield
    # stop it on shutdown
    stop_daemon()


Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(channels.router, prefix="/api/channels")
app.include_router(medias.router, prefix="/api/medias")
app.include_router(presets.router, prefix="/api/presets")
app.include_router(daemon.router, prefix="/api/daemon")

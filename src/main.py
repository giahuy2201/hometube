from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import signal

from core.database import Base, engine
from daemon.service import stop_daemon, start_daemon
import daemon.router as daemon
import medias.router as medias
import presets.router as presets


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Stop the daemon on shutdown signal (Ctrl-C)
    signal.signal(signal.SIGINT, stop_daemon)
    yield


Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

start_daemon()

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

app.include_router(medias.router, prefix="/api/medias")
app.include_router(presets.router, prefix="/api/presets")
app.include_router(daemon.router, prefix="/api/daemon")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from workers.daemon import daemon
import signal

import library.router as library
import presets.router as presets


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Add mock data
    
    # Stop the daemon on shutdown signal (Ctrl-C)
    signal.signal(signal.SIGINT, daemon.stop)
    yield


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

app.include_router(library.router, prefix="/api/medias")
app.include_router(presets.router, prefix="/api/presets")

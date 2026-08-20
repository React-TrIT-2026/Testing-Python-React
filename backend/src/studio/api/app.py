from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from studio.api.errors import register_handlers
from studio.api.routers import bookings, ops, schedule
from studio.api.schemas import ResetIn


def create_app() -> FastAPI:
    app = FastAPI(
        title="Studio Bookings",
        version="1.0.0",
        description="Fitness studio class booking API",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("STUDIO_CORS_ORIGINS", "http://localhost:5173").split(","),
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_handlers(app)
    app.include_router(schedule.router, prefix="/api")
    app.include_router(bookings.router, prefix="/api")
    app.include_router(ops.router, prefix="/api")

    @app.get("/api/health", tags=["ops"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/test/reset", tags=["ops"], include_in_schema=False)
    def reset(payload: ResetIn | None = None) -> dict[str, object]:
        from studio.api.dependencies import (  # noqa: PLC0415
            STORAGE,
            force_clock,
            reset_memory_storage,
        )

        if STORAGE != "memory":
            return {"reset": False, "reason": "only available with STUDIO_STORAGE=memory"}

        force_clock(payload.now if payload else None)
        reset_memory_storage()
        return {"reset": True, "now": payload.now.isoformat() if payload and payload.now else None}

    return app


app = create_app()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from pathlib import Path
from app.routes import reservations, properties

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(
    title="Sistema de Reservas",
    description="API para gestionar reservas con OCR y Google Calendar",
    version="0.1.0"
)

# CORS para permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas API (deben venir antes de los archivos estáticos)
app.include_router(properties.router)
app.include_router(reservations.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Servir archivos estáticos (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    # Servir archivos estáticos en /static/
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    # Servir index.html en la raíz y en otros paths
    @app.get("/")
    async def root():
        with open(frontend_path / "index.html", "r", encoding="utf-8") as f:
            return f.read()

    from fastapi.responses import HTMLResponse

    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def serve_spa(full_path: str):
        # Si no es una ruta API y no es un archivo estático conocido, servir index.html (SPA)
        if full_path.startswith("api/") or full_path.startswith("static/"):
            return {"error": "Not found"}

        file_path = frontend_path / full_path
        if file_path.exists() and file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        # Por defecto, servir index.html
        with open(frontend_path / "index.html", "r", encoding="utf-8") as f:
            return f.read()
else:
    @app.get("/")
    def read_root():
        return {"message": "Frontend no encontrado. Asegúrate de que la carpeta frontend existe."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

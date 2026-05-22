from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webapp.routes import plans

app = FastAPI(title="Intizom AI Web App API", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans.router, prefix="/api/webapp")


@app.get("/health")
async def health():
    return {"status": "ok"}

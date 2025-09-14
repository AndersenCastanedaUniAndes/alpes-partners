from fastapi import FastAPI
from alpespartners.api import marketing_influencers, tracking

app = FastAPI()

# incluir routers de otros módulos si existen
app.include_router(marketing_influencers.router)
app.include_router(tracking.router)

@app.get("/")
def root():
    return {"message": "OK"}

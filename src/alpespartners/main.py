from fastapi import FastAPI
from alpespartners.api import marketing_influencers

app = FastAPI()

# incluir routers de otros módulos si existen
app.include_router(marketing_influencers.router)

@app.get("/")
def root():
    return {"message": "OK"}

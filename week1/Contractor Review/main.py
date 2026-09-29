from fastapi import FastAPI
from reports import router as reports_router


app = FastAPI(title="Firm Intelligence API")

app.include_router(reports_router)

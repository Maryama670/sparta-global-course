from fastapi import FastAPI

import firms
import people

app = FastAPI()

app.include_router(firms.router)
app.include_router(people.router)


@app.get("/health")
def health():
    return {"status": "ok"}

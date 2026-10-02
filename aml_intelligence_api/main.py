Main.py 
is the entry point for the whole FastPI application it connects everything together 
app = FastAPI()

app.include_router(alerts.router)
app.include_router(accounts.router)
app.include_router(analysts.router)
app.include_router(cases.router)
app.include_router(knowledge.router)
app.include_router(agent_api.router)

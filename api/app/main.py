from fastapi import FastAPI
from app.api.routes import contacts, auth, invoices

app = FastAPI(title="Chift Case API")

app.include_router(
    contacts.router,
    prefix="/contacts",
    tags=["Contacts"]
)


app.include_router(
    invoices.router,
    prefix="/invoices",
    tags=["Invoices"]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

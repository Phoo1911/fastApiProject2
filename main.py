from fastapi import FastAPI, Form, Request, RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Sample data structure to store transactions
transactions = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "transactions": transactions})

@app.post("/add_transaction")
async def add_transaction(
    request: Request,
    transaction_amount: float = Form(...),
    transaction_type: str = Form(...),
    transaction_description: str = Form(...)
):
    transaction = {
        "amount": transaction_amount,
        "type": transaction_type,
        "description": transaction_description
    }
    transactions.append(transaction)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete_transaction/{transaction_id}")
async def delete_transaction(transaction_id: int):
    if 0 <= transaction_id < len(transactions):
        transactions.pop(transaction_id)
    return RedirectResponse(url="/", status_code=303)

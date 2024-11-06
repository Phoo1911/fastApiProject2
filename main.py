from fastapi import FastAPI, Depends, Form, HTTPException, Request, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database import SessionLocal
from crud import get_transactions, add_transaction, delete_transaction

app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET route to display transactions and render the template
@app.get("/")
async def read_transactions(request: Request, db: Session = Depends(get_db)):
    transactions = get_transactions(db)
    return templates.TemplateResponse("index.html", {"request": request, "transactions": transactions})

# POST route to add a new transaction
@app.post("/transactions/add")
async def create_transaction(
    amount: float = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    add_transaction(db, type=type, amount=amount, description=description)
    return RedirectResponse(url="/", status_code=303)

# POST route to delete a transaction
@app.post("/transactions/delete/{transaction_id}")
async def remove_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = delete_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return RedirectResponse(url="/", status_code=303)

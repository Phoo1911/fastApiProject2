
from sqlalchemy.orm import Session
from models import Transaction

def get_transactions(db: Session):
    return db.query(Transaction).all()

def add_transaction(db: Session, type: str, amount: float, description: str):
    db_transaction = Transaction(type=type, amount=amount, description=description)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return db_transaction
    return None

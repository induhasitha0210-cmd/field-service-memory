from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("")
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).order_by(Customer.name.asc()).all()
    return [c.to_dict() for c in customers]


@router.get("/{cust_id}")
def get_customer(cust_id: str, db: Session = Depends(get_db)):
    cust = db.query(Customer).filter(Customer.id == cust_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail=f"Customer {cust_id} not found")
    data = cust.to_dict()
    data["sites"] = [s.to_dict() for s in cust.sites]
    data["equipment"] = [e.to_dict() for e in cust.equipment]
    return data

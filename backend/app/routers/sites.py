from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Site

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("")
def list_sites(customer_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Site)
    if customer_id:
        query = query.filter(Site.customer_id == customer_id)
    sites = query.order_by(Site.name.asc()).all()
    return [s.to_dict() for s in sites]


@router.get("/{site_id}")
def get_site(site_id: str, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail=f"Site {site_id} not found")
    data = site.to_dict()
    data["equipment"] = [e.to_dict() for e in site.equipment]
    return data

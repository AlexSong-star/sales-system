from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from ..database import get_db
from ..models import Customer, Inquiry
from ..schemas import CustomerCreate, CustomerUpdate, CustomerOut, CustomerDetailOut

router = APIRouter(prefix="/api/customers", tags=["客户"])


@router.get("", response_model=list[CustomerOut])
def list_customers(
    level: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Customer)
    if level:
        q = q.filter(Customer.level == level)
    if status:
        q = q.filter(Customer.status == status)
    if source:
        q = q.filter(Customer.source == source)
    if search:
        q = q.filter(
            (Customer.name.contains(search)) | (Customer.company.contains(search))
        )
    customers = q.order_by(Customer.created_at.desc()).all()

    # 附加询盘数量
    result = []
    for c in customers:
        inq_count = db.query(func.count(Inquiry.id)).filter(Inquiry.customer_id == c.id).scalar()
        out = CustomerOut.model_validate(c)
        out.inquiry_count = inq_count or 0
        result.append(out)
    return result


@router.get("/{customer_id}", response_model=CustomerDetailOut)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return customer


@router.post("", response_model=CustomerOut)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.id == data.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"客户 {data.id} 已存在")
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    out = CustomerOut.model_validate(customer)
    out.inquiry_count = 0
    return out


@router.patch("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: str, data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(customer, k, v)
    db.commit()
    db.refresh(customer)
    inq_count = db.query(func.count(Inquiry.id)).filter(Inquiry.customer_id == customer.id).scalar()
    out = CustomerOut.model_validate(customer)
    out.inquiry_count = inq_count or 0
    return out


@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    db.delete(customer)
    db.commit()
    return {"ok": True}

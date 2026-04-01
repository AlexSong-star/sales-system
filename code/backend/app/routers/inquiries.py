from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Inquiry, Reply
from ..schemas import InquiryCreate, InquiryUpdate, InquiryOut, ReplyCreate, ReplyOut

router = APIRouter(prefix="/api/inquiries", tags=["询盘"])


@router.get("", response_model=list[InquiryOut])
def list_inquiries(
    channel: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Inquiry)
    if channel:
        q = q.filter(Inquiry.channel == channel)
    if status:
        q = q.filter(Inquiry.status == status)
    if customer_id:
        q = q.filter(Inquiry.customer_id == customer_id)
    inquiries = q.order_by(Inquiry.created_at.desc()).all()
    return inquiries


@router.get("/{inquiry_id}", response_model=InquiryOut)
def get_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="询盘不存在")
    return inquiry


@router.post("", response_model=InquiryOut)
def create_inquiry(data: InquiryCreate, db: Session = Depends(get_db)):
    inquiry = Inquiry(**data.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.patch("/{inquiry_id}", response_model=InquiryOut)
def update_inquiry(inquiry_id: int, data: InquiryUpdate, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="询盘不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(inquiry, k, v)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.delete("/{inquiry_id}")
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="询盘不存在")
    db.delete(inquiry)
    db.commit()
    return {"ok": True}


# --- Replies ---
@router.get("/{inquiry_id}/replies", response_model=list[ReplyOut])
def list_replies(inquiry_id: int, db: Session = Depends(get_db)):
    replies = db.query(Reply).filter(Reply.inquiry_id == inquiry_id).order_by(Reply.created_at.asc()).all()
    return replies


@router.post("/{inquiry_id}/replies", response_model=ReplyOut)
def add_reply(inquiry_id: int, data: ReplyCreate, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="询盘不存在")
    reply = Reply(inquiry_id=inquiry_id, content=data.content)
    db.add(reply)
    # 自动更新询盘状态为已回复
    inquiry.status = "replied"
    db.commit()
    db.refresh(reply)
    return reply

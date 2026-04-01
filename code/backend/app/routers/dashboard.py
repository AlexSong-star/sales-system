from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Inquiry
from ..schemas import DashboardStats, TrendPoint

router = APIRouter(prefix="/api/dashboard", tags=["仪表盘"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)

    today_q = db.query(func.count(Inquiry.id)).filter(Inquiry.created_at >= today_start)
    week_q = db.query(func.count(Inquiry.id)).filter(Inquiry.created_at >= week_start)
    pending_q = db.query(func.count(Inquiry.id)).filter(Inquiry.status == "pending")
    closed_q = db.query(func.count(Inquiry.id)).filter(Inquiry.status == "closed")
    email_q = db.query(func.count(Inquiry.id)).filter(Inquiry.channel == "email")
    whatsapp_q = db.query(func.count(Inquiry.id)).filter(Inquiry.channel == "whatsapp")
    alibaba_q = db.query(func.count(Inquiry.id)).filter(Inquiry.channel == "alibaba")

    return DashboardStats(
        today_inquiries=today_q.scalar() or 0,
        week_inquiries=week_q.scalar() or 0,
        pending=pending_q.scalar() or 0,
        closed=closed_q.scalar() or 0,
        email_count=email_q.scalar() or 0,
        whatsapp_count=whatsapp_q.scalar() or 0,
        alibaba_count=alibaba_q.scalar() or 0,
    )


@router.get("/trend", response_model=list[TrendPoint])
def get_trend(days: int = 7, db: Session = Depends(get_db)):
    """返回最近N天的每日询盘数量，按渠道分组"""
    now = datetime.now()
    points = []
    for i in range(days - 1, -1, -1):
        day = (now - timedelta(days=i)).date()
        next_day = day + timedelta(days=1)
        email_c = db.query(func.count(Inquiry.id)).filter(
            Inquiry.channel == "email",
            Inquiry.created_at >= datetime.combine(day, datetime.min.time()),
            Inquiry.created_at < datetime.combine(next_day, datetime.min.time())
        ).scalar() or 0
        whatsapp_c = db.query(func.count(Inquiry.id)).filter(
            Inquiry.channel == "whatsapp",
            Inquiry.created_at >= datetime.combine(day, datetime.min.time()),
            Inquiry.created_at < datetime.combine(next_day, datetime.min.time())
        ).scalar() or 0
        alibaba_c = db.query(func.count(Inquiry.id)).filter(
            Inquiry.channel == "alibaba",
            Inquiry.created_at >= datetime.combine(day, datetime.min.time()),
            Inquiry.created_at < datetime.combine(next_day, datetime.min.time())
        ).scalar() or 0
        points.append(TrendPoint(
            date=day.strftime("%m-%d"),
            email=email_c, whatsapp=whatsapp_c, alibaba=alibaba_c
        ))
    return points

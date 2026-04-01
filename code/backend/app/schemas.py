from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Reply ---
class ReplyBase(BaseModel):
    content: str


class ReplyCreate(ReplyBase):
    pass


class ReplyOut(ReplyBase):
    id: int
    inquiry_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Inquiry ---
class InquiryBase(BaseModel):
    channel: str = "email"
    product: str = ""
    quantity: str = ""
    specs: str = ""
    destination: str = ""
    intent: str = "medium"
    content: str = ""
    status: str = "pending"
    summary: str = ""


class InquiryCreate(InquiryBase):
    customer_id: str


class InquiryUpdate(BaseModel):
    status: Optional[str] = None
    summary: Optional[str] = None


class InquiryOut(InquiryBase):
    id: int
    customer_id: str
    created_at: datetime
    updated_at: datetime
    replies: list[ReplyOut] = []

    class Config:
        from_attributes = True


# --- Customer ---
class CustomerBase(BaseModel):
    name: str
    company: str = ""
    email: str = ""
    country: str = ""
    level: str = "C"
    status: str = "pending"
    source: str = "email"
    priority: str = "medium"
    next_step: str = ""
    expected_close: str = ""


class CustomerCreate(CustomerBase):
    id: str  # 手动指定，如 C001


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    level: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    next_step: Optional[str] = None
    expected_close: Optional[str] = None


class CustomerOut(CustomerBase):
    id: str
    created_at: datetime
    inquiry_count: int = 0

    class Config:
        from_attributes = True


class CustomerDetailOut(CustomerBase):
    id: str
    created_at: datetime
    inquiries: list[InquiryOut] = []

    class Config:
        from_attributes = True


# --- Dashboard ---
class DashboardStats(BaseModel):
    today_inquiries: int = 0
    week_inquiries: int = 0
    pending: int = 0
    closed: int = 0
    email_count: int = 0
    whatsapp_count: int = 0
    alibaba_count: int = 0


class TrendPoint(BaseModel):
    date: str
    email: int
    whatsapp: int
    alibaba: int

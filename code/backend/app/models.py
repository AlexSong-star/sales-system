from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base


class CustomerLevel(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"


class CustomerStatus(str, enum.Enum):
    pending = "pending"
    following = "following"
    closed = "closed"
    lost = "lost"


class InquiryStatus(str, enum.Enum):
    pending = "pending"
    replied = "replied"
    following = "following"
    closed = "closed"
    invalid = "invalid"


class Channel(str, enum.Enum):
    email = "email"
    whatsapp = "whatsapp"
    alibaba = "alibaba"


class IntentLevel(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)          # C001, C002...
    name = Column(String, nullable=False)
    company = Column(String, default="")
    email = Column(String, default="")
    country = Column(String, default="")
    level = Column(String, default="C")             # A / B / C
    status = Column(String, default="pending")     # pending / following / closed / lost
    source = Column(String, default="email")       # email / whatsapp / alibaba
    priority = Column(String, default="medium")     # high / medium / low / closed
    next_step = Column(String, default="")
    expected_close = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())

    inquiries = relationship("Inquiry", back_populates="customer", cascade="all, delete-orphan")


class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    channel = Column(String, default="email")      # email / whatsapp / alibaba
    product = Column(String, default="")
    quantity = Column(String, default="")
    specs = Column(Text, default="")
    destination = Column(String, default="")
    intent = Column(String, default="medium")      # high / medium / low
    content = Column(Text, default="")             # 原始询盘正文
    status = Column(String, default="pending")     # pending / replied / following / closed / invalid
    summary = Column(Text, default="")            # AI摘要
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="inquiries")
    replies = relationship("Reply", back_populates="inquiry", cascade="all, delete-orphan")


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    inquiry_id = Column(Integer, ForeignKey("inquiries.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    inquiry = relationship("Inquiry", back_populates="replies")

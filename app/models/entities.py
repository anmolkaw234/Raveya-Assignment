from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

from app.db.session import Base


class PromptLog(Base):
    __tablename__ = "prompt_logs"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(100), nullable=False)
    request_payload = Column(JSON, nullable=False)
    prompt_text = Column(Text, nullable=False)
    response_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ProductAnalysis(Base):
    __tablename__ = "product_analyses"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)
    primary_category = Column(String(120), nullable=False)
    sub_category = Column(String(120), nullable=False)
    seo_tags = Column(JSON, nullable=False)
    sustainability_filters = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String(255), nullable=False)
    budget = Column(Integer, nullable=False)
    product_mix = Column(JSON, nullable=False)
    cost_breakdown = Column(JSON, nullable=False)
    impact_positioning_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

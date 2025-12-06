from sqlalchemy import Column, Integer, String, Date, Numeric, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String)
    asset_type = Column(String)
    status = Column(String)
    purchase_date = Column(Date)
    warranty_expiry = Column(Date)
    assigned_to = Column(String)
    cost = Column(Numeric)
    last_updated = Column(TIMESTAMP)

class AssetLog(Base):
    __tablename__ = "asset_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(TIMESTAMP)

from sqlalchemy import (
    Column,
    Enum,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, declarative_base

from market.api import schemas

Base = declarative_base()


class ShopUnit(Base):
    __tablename__ = "shop_units"
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(Enum(schemas.ShopUnitType), nullable=False)


class Category(Base):
    __tablename__ = "categories"
    uuid = Column(UUID(as_uuid=True), ForeignKey("shop_units.uuid", ondelete="CASCADE"), primary_key=True)

    history = relationship("CategoryHistory", foreign_keys="CategoryHistory.uuid")


class Offer(Base):
    __tablename__ = "offers"
    uuid = Column(UUID(as_uuid=True), ForeignKey("shop_units.uuid", ondelete="CASCADE"), primary_key=True)

    history = relationship("OffersHistory", foreign_keys="OffersHistory.uuid")


class CategoryHistory(Base):
    __tablename__ = "categories_history"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete='SET NULL'), nullable=True, )
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())


class OffersHistory(Base):
    __tablename__ = "offers_history"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), ForeignKey("offers.uuid", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete='SET NULL'), nullable=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Integer, nullable=True)

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    )
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship)

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.dialects.sqlite import DATE

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    date = Column(DATE)

    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = 'invoice_item'
    id = Column(Integer, primary_key=True)
    units = Column(Integer)
    description = Column(String)
    amount = Column(Numeric)    # Numeric is the Decimal rep in SQLite

    invoice_id = Column(ForeignKey('invoice.id'))
    invoice = relationship('Invoice', back_populates='items')

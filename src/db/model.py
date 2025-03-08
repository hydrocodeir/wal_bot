from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import threading
import time

# creat database
engine = create_engine("sqlite:///data/wal.db")
base = declarative_base()
session = sessionmaker(bind=engine)()
metadata = MetaData()
metadata.reflect(bind=engine)


class admins(base):
    __tablename__ = "admins"

    chat_id = Column("chat_id", Integer, unique=True)
    user_name = Column("user_name", String, unique=True, primary_key=True)
    password = Column("password", String, unique=True, primary_key=True)
    inb_id = Column("inb_id", Integer)
    traffic = Column("traffic", String)
    debt = Column("debt", Integer, nullable=False, default=0)
    debt_days = Column("debt_days", Integer, default=0)
    status = Column("status", Boolean, default=True)


class priceing(base):
    __tablename__ = "priceing"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    traffic = Column("traffic", Integer)
    price = Column("price", Integer)


class TrafficPrice(base):
    __tablename__ = "traffic_price"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    price = Column("price", Integer)
    dead_line = Column("dead_line", Integer, default=30)


class Card(base):
    __tablename__ = "card_number"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_number = Column(String, nullable=False)


class HelpMessage(base):
    __tablename__ = "help_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)


class RegisteringMessage(base):
    __tablename__ = "registering_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)


class BotSettings(base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_notif = Column("start_notif", Boolean, default=True)
    create_notif = Column("creat_notif", Boolean, default=True)
    delete_notif = Column("delete_notif", Boolean, default=True)
    debt_system = Column("debt_system", Boolean, default=False)


base.metadata.create_all(engine)



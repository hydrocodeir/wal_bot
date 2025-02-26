from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base


# creat database
engine = create_engine("sqlite:///data/wal.db")
base = declarative_base()
session = sessionmaker(bind=engine)()


class admins(base):
    __tablename__ = "admins"

    chat_id = Column("chat_id", Integer, unique=True)
    user_name = Column("user_name", String, unique=True, primary_key=True)
    password = Column("password", String, unique=True, primary_key=True)
    inb_id = Column("inb_id", Integer)
    debt = Column("debt", Integer, default=0)
    traffic = Column("traffic", String)


class priceing(base):
    __tablename__ = "priceing"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    traffic = Column("traffic", Integer)
    price = Column("price", Integer)

class TrafficPrice(base):
    __tablename__ = "traffic_price"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    price = Column("price", Integer)


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


# default settings
def initialize_settings():
    try:
        settings = session.query(BotSettings).first()
        if not settings:
            difault_settings = BotSettings(
                start_notif=True, create_notif=True, delete_notif=True
            )
            session.add(difault_settings)
            session.commit()
        else:
            pass
    except:
        pass


initialize_settings()


# settings query
class SettingsQuery:
    def change_start_notif(self, new_sttings):
        try:
            update = session.query(BotSettings).first()
            if update:
                update.start_notif = new_sttings
                session.commit()
                return True
            else:
                return False
        except:
            return False

    def show_start_notif(self):
        try:
            settings = session.query(BotSettings).first()
            if settings:
                return settings.start_notif
            else:
                return False
        except:
            return False

    def change_create_notif(self, new_setting):
        try:
            updata = session.query(BotSettings).first()
            if updata:
                updata.create_notif = new_setting
                session.commit()
                return True
            else:
                return False
        except:
            return False

    def show_create_notif(self):
        try:
            settings = session.query(BotSettings).first()
            if settings:
                return settings.create_notif
            else:
                return False
        except:
            return False

    def change_delete_notif(self, new_setting):
        try:
            update = session.query(BotSettings).first()
            if update:
                update.delete_notif = new_setting
                session.commit()
                return True
            else:
                return False
        except:
            return False

    def show_delete_notif(self):
        try:
            settings = session.query(BotSettings).first()
            if settings:
                return settings.delete_notif
            else:
                return False
        except:
            return False
        
    def change_debt_system(self, new_setting):
        try:
            update = session.query(BotSettings).first()
            if update:
                update.debt_system = new_setting
                session.commit()
                return True
            else:
                return False
        except:
            return False
        
    def show_debt_stasus(self):
        try:
            status = session.query(BotSettings).first()
            if status:
                return status.debt_system
            else:
                return False
        except:
            return False

setting_query = SettingsQuery()

# traffic price
class TrafficPriceQuery:
    def add_price(self, new_price):
        try:
            price = session.query(TrafficPrice).filter(TrafficPrice.id == 1).first()
            if price:
                price.price = new_price
            else:
                price = TrafficPrice(id=1, price=new_price)
                session.add(price)
            session.commit()
            return True
        except:
            return False
        
    def show_price(self):
        try:
            price = session.query(TrafficPrice).filter(TrafficPrice.id == 1).first()
            if not price:
                return "⚠️ تنظیم نشده"
            price_data = price.price
            return price_data
        except:
            return False

traffic_price_query = TrafficPriceQuery()


# help message query
class MessageQuery:
    def add_message(self, new_message):
        try:
            message = session.query(HelpMessage).filter(HelpMessage.id == 1).first()
            if message:
                message.message = new_message
            else:
                message = HelpMessage(id=1, message=new_message)
                session.add(message)
            session.commit()
            return True
        except:
            return False

    def show_message(self):
        try:
            message = session.query(HelpMessage).filter(HelpMessage.id == 1).first()
            if not message:
                return {"message": "⚠️ متن راهنما خالی است"}
            message_data = {"message": message.message}
            return message_data
        except:
            return False


help_message_query = MessageQuery()


# register message query
class RegisterQuery:
    def add_message(sel, new_message):
        try:
            message = (
                session.query(RegisteringMessage)
                .filter(RegisteringMessage.id == 1)
                .first()
            )
            if message:
                message.message = new_message
            else:
                message = RegisteringMessage(id=1, message=new_message)
                session.add(message)
            session.commit()
            return True
        except:
            return False

    def show_message(self):
        try:
            message = (
                session.query(RegisteringMessage)
                .filter(RegisteringMessage.id == 1)
                .first()
            )
            if not message:
                return {"message": "⚠️ متن قوانین ثبت نام خالی است"}
            message_data = {"message": message.message}
            return message_data
        except:
            return False


registering_message = RegisterQuery()


# card query
class CardQuery:
    def add(self, new_card):
        try:
            card = session.query(Card).filter(Card.id == 1).first()
            if card:
                card.card_number = new_card
            else:
                card = Card(id=1, card_number=new_card)
                session.add(card)
            session.commit()
            return True
        except:
            return False

    def show_card(self):
        try:
            card = session.query(Card).filter(Card.id == 1).first()
            if not card:
                return {"card_number": "123456789"}
            card_data = {"card_number": card.card_number}
            return card_data
        except:
            return False


card_number_query = CardQuery()


# pricing query
class PriceQuery:
    def add_plan(self, traffic, price):
        try:
            new_plan = priceing(traffic=traffic, price=price)
            session.add(new_plan)
            session.commit()
            return True
        except:
            return False

    def delete_plan(self, id):
        try:
            delete = session.query(priceing).filter(priceing.id == id).first()
            session.delete(delete)
            session.commit()
            self.reorder_ids()
            return True
        except:
            return False

    def edite_plan(self, id, traffic, price):
        try:
            update = (
                session.query(priceing)
                .filter(priceing.id == id)
                .update({"traffic": traffic, "price": price})
            )
            session.commit()
            if update:
                return True
            else:
                return False
        except:
            return False

    def reorder_ids(self):
        try:
            plans = session.query(priceing).order_by(priceing.id).all()
            for index, plan in enumerate(plans, start=1):
                plan.id = index
            session.commit()
            return True
        except:
            return False

    def show_plans(self):
        try:
            plans = session.query(priceing).all()
            pricing_list = [
                {"id": price.id, "traffic": price.traffic, "price": price.price}
                for price in plans
            ]
            return pricing_list
        except:
            False

    def get_plan(self, id):
        try:
            plan = session.query(priceing).filter(priceing.id == id).first()
            if not plan:
                return False
            data = {
                "traffic": plan.traffic,
                "price": plan.price,
            }
            return data
        except:
            return False


price_query = PriceQuery()


# admins query
class AdminsQuery:
    def add_admin(self, user_name, password, traffic, inb_id):
        try:
            new_admin = admins(
                user_name=user_name, password=password, traffic=traffic, inb_id=inb_id
            )
            session.add(new_admin)
            session.commit()
            return True
        except:
            return False

    def change_inb(self, user_name, inb_id):
        try:
            update = (
                session.query(admins)
                .filter(admins.user_name == user_name)
                .update({"inb_id": inb_id})
            )
            session.commit()
            return True
        except:
            return False

    def add_traffic(self, user_name, traffic):
        try:
            admin = session.query(admins).filter(admins.user_name == user_name).first()
            if admin:
                if admin.traffic.lower() =="false":
                    admin.traffic = traffic
                else:    
                    admin.traffic += traffic
                session.commit()
                return True
            return False
        except:
            return False
    def set_debt_system(self, chat_id, traffic):
        try:
            admin = session.query(admins).filter(admins.chat_id == chat_id).first()
            if admin:
                admin.traffic = traffic
                session.commit()
                return True
            return False
        except:
            return False

    def delete_admin(self, user_name):
        try:
            delete = session.query(admins).filter(admins.user_name == user_name).first()
            session.delete(delete)
            session.commit()
            return True
        except:
            return False

    def show_admins(self):
        try:
            select_admins = session.query(admins).all()
            admins_list = [
                {
                    "user_name": admin.user_name,
                    "password": admin.password,
                    "traffic": admin.traffic,
                    "inb_id": admin.inb_id,
                    "debt": admin.debt
                }
                for admin in select_admins
            ]
            return admins_list
        except:
            False

    def add_chat_id(self, user_name, password, chat_id):
        try:
            check = check = (
                session.query(admins)
                .filter_by(user_name=user_name, password=password)
                .all()
            )
            if check:
                update = (
                    session.query(admins)
                    .filter(admins.user_name == user_name)
                    .update({"chat_id": chat_id})
                )
                session.commit()
                return True
            else:
                return False
        except:
            False

    def remove_chat_id(self, chat_id):
        try:
            update = (
                session.query(admins)
                .filter(admins.chat_id == chat_id)
                .update({"chat_id": None})
            )
            session.commit()
            return True
        except:
            return False

    def admin_data(self, chat_id):
        try:
            admin = session.query(admins).filter(admins.chat_id == chat_id).first()
            if not admin:
                return False
            data = {
                "user_name": admin.user_name,
                "password": admin.password,
                "traffic": admin.traffic,
                "inb_id": admin.inb_id,
                "debt": admin.debt
            }
            return data
        except:
            return False
        
    def clear_debt(self, chat_id):
        try:
            update = (
                session.query(admins)
                .filter(admins.chat_id == chat_id)
                .update({"debt": 0})
            )
            session.commit()
            return True
        except:
            return False


    def reduce_traffic(self, chat_id, delta):
        try:
            admin = session.query(admins).filter(admins.chat_id == chat_id).first()
            if not admin:
                return False
            if admin.traffic.lower() == "false":
                admin.debt += delta
            else:
                new_traffic = int(admin.traffic) - abs(delta)
                if new_traffic < 0:
                    new_traffic = 0
                admin.traffic = str(new_traffic)
            session.commit()
            return True
        except:
            return False

    def admin_approval(self, chat_id):
        try:
            approv = session.query(admins).filter(admins.chat_id == chat_id).all()
            if approv:
                return True
            else:
                return False
        except:
            return False


admins_query = AdminsQuery()

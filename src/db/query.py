from db.model import session, BotSettings, TrafficPrice, admins, priceing, HelpMessage, RegisteringMessage, Card, Panels
from handlers.notifications import notif_setting
import threading

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
        
    def change_deadline_notif(self, new_setting):
        try:
            update = session.query(BotSettings).first()
            if update:
                update.deadline_notif = new_setting
                session.commit()
                return True
            else:
                return False
        except:
            return False
        
    def show_deadline_notif(self):
        try:
            setting = session.query(BotSettings).first()
            if setting:
                return setting.deadline_notif
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
        
    def add_dead_line(self, new_dead_line):
        try:
            dead_line = session.query(TrafficPrice).filter(TrafficPrice.id == 1).first()
            if dead_line:
                dead_line.dead_line = new_dead_line
            else:
                dead_line = TrafficPrice(id=1, dead_line=new_dead_line)
                session.add(dead_line)
            session.commit()
            return True
        except:
            return False
        
    def show_dead_line(self):
        try:
            dead_line = session.query(TrafficPrice).filter(TrafficPrice.id == 1).first()
            data = dead_line.dead_line
            return data
        except:
            return False




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
            return False

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



# admins query
class AdminsQuery:
    def add_admin(self, user_name, password, traffic, panel_id, inb_id):
        try:
            new_admin = admins(
                user_name=user_name, password=password, traffic=traffic, panel_id=panel_id, inb_id=inb_id
            )
            session.add(new_admin)
            session.commit()
            return True
        except:
            return False
        
    def change_panel(self, user_name, panel_id):
        try:
            update = (
                session.query(admins)
                .filter(admins.user_name == user_name)
                .update({"panel_id": panel_id})
            )
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
                    new_traffic = int(admin.traffic) + int(traffic)
                    admin.traffic = str(new_traffic)
                session.commit()
                return True
            return False
        except:
            return False
        
    def set_debt_system(self, chat_id, traffic, debt, dead_line):
        try:
            admin = session.query(admins).filter(admins.chat_id == chat_id).first()
            if admin:
                admin.traffic = traffic
                admin.debt = debt
                admin.debt_days = dead_line
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
                    "panel_id": admin.panel_id,
                    "inb_id": admin.inb_id,
                    "debt": admin.debt
                }
                for admin in select_admins
            ]
            return admins_list
        except:
            return False

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
            return False

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
                return {
                    "user_name": None,
                    "password": None,
                    "status": False,
                    "traffic": "0",
                    "inb_id": None,
                    "debt": 0,
                    "debt_days": 0
                }
            data = {
                "user_name": admin.user_name,
                "password": admin.password,
                "status": admin.status,
                "traffic": admin.traffic,
                "inb_id": admin.inb_id,
                "debt": admin.debt,
                "debt_days": admin.debt_days,
                "panel_id": admin.panel_id
            }
            return data
        except:
            return {
                "user_name": None,
                "password": None,
                "status": False,
                "traffic": "0",
                "inb_id": None,
                "debt": 0,
                "debt_days": 0
            }
        
    def clear_debt(self, chat_id, new_dead_line):
        try:
            update = (
                session.query(admins)
                .filter(admins.chat_id == chat_id)
                .update({"debt": 0, "debt_days": new_dead_line})
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
                admin.debt += int(delta)
            else:
                new_traffic = int(admin.traffic) - abs(int(delta))
                if new_traffic < 0:
                    new_traffic = 0
                admin.traffic = str(new_traffic)
            session.commit()
            return True
        except:
            return False
        
    def reduse_traffic_by_username(self, user_name, delta):
        try:
            admin = session.query(admins).filter(admins.user_name == user_name).first()
            if admin.traffic.lower() == "false":
                return False
            else:
                new_traffic = int(admin.traffic) - delta
                if new_traffic < 0:
                    new_traffic = 0
                admin.traffic = str(new_traffic)
                session.commit()
                return True
        except:
            return False
        
    def change_admin_status(self, user_name, new_status):
        try:
            admin = session.query(admins).filter(admins.user_name == user_name).first()
            admin.status = new_status
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
        
    def approv_for_modify(self, user_name):
        try:
            approve = session.query(admins).filter(admins.user_name == user_name).first()
            if approve:
                return True
            else:
                return False
        except:
            return False

    def admin_data_for_modify(self, user_name):
        try:
            admin = session.query(admins).filter(admins.user_name == user_name).first()
            data = {
                "chat_id": admin.chat_id,
                "user_name": admin.user_name,
                "password": admin.password,
                "status": admin.status,
                "traffic": admin.traffic,
                "panel_id": admin.panel_id,
                "inb_id": admin.inb_id,
                "debt": admin.debt,
                "debt_days": admin.debt_days
            }
            return data
        except:
            return False
        
    def descrease_debt_days(self):
        admins_list = session.query(admins).all()
        for admin in admins_list:
            if admin.debt_days > 0:
                admin.debt_days -= 1
                if setting_query.show_deadline_notif():
                    if admin.debt_days <= 3:
                        notif_setting.deadline_notif(admin.chat_id, admin.user_name, admin.debt_days, admin.debt)

        session.commit()
        threading.Timer(86400, self.descrease_debt_days).start()

# panels query
class PanelsQuery:
    def add_panel(self, name, address, sub, username, password):
        try:
            new_panel = Panels(
                name = name,
                address = address,
                sub = sub,
                username = username,
                password = password
            )
            session.add(new_panel)
            session.commit()
            return True
        except:
            return False

    def show_panels(self):
        try:
            panels = session.query(Panels).all()
            panels_data = [
                {
                    "id": panel.id,
                    "name": panel.name,
                    "address": panel.address,
                    "sub": panel.sub,
                    "username": panel.username,
                    "password": panel.password
                }
                for panel in panels
            ]
            return panels_data
        except:
            return False
        
    def delete_panel(self, id):
        try:
            delete = session.query(Panels).filter(Panels.id == id).first()
            session.delete(delete)
            session.commit()
            return True
        except:
            return False
        
    def edit_panel(self, id, name, address, sub, username, password):
        try:
            update = (
                session.query(Panels)
                .filter(Panels.id == id)
                .update({"name": name, "address": address, "sub": sub, "username": username, "password": password})
            )
            session.commit()
            return True
        except:
            return False
        
    def get_panel_data(self, id):
        try:
            panel = session.query(Panels).filter(Panels.id == id).first()
            if not panel:
                return False
            data = {
                "address": panel.address,
                "username": panel.username,
                "password": panel.password,
                "sub": panel.sub,
                "name": panel.name
            }
            
            return data
        except:
            return False    
    
    def approve_panel_for_modify(self, id):
        try:
            approve = session.query(Panels).filter(Panels.id == id).first()
            if approve:
                return True
            else:
                return False
        except:
            return False
        

setting_query = SettingsQuery()
traffic_price_query = TrafficPriceQuery()
help_message_query = MessageQuery()
registering_message = RegisterQuery()
card_number_query = CardQuery()
price_query = PriceQuery()
admins_query = AdminsQuery()
admins_query.descrease_debt_days()
panels_query = PanelsQuery()

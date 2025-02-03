from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


# creat database
engine = create_engine('sqlite:///src/db/wal.db')
base = declarative_base()
session = sessionmaker(bind=engine)()

class admins(base):
    __tablename__ = 'admins'

    chat_id = Column('chat_id', Integer, unique=True)
    user_name = Column('user_name', String, unique=True, primary_key=True)
    password = Column('password', String)
    traffic = Column('traffic', Integer)
    inb_id = Column('inb_id', Integer)

base.metadata.create_all(engine)

# admins query
class AdminsQuery:
    def add_admin(self, user_name, password, traffic, inb_id):
        try:
            new_admin = admins(
                user_name=user_name,
                password=password,
                traffic=traffic,
                inb_id=inb_id
            )
            session.add(new_admin)
            session.commit()
            return True
        except:
            return False
        
    def change_inb(self, user_name, inb_id):
        try:
            update = session.query(admins).filter(admins.user_name==user_name).update({'inb_id':inb_id})
            session.commit()
            return True
        except:
            return False
        
    def add_traffic(self, user_name, traffic):
        try:
            admin = session.query(admins).filter(admins.user_name==user_name).first()
            if admin:
                admin.traffic += traffic
                session.commit()
                return True
            return False
        except:
            return False
        
    def delete_admin(self, user_name):
        try:
            delete = session.query(admins).filter(admins.user_name==user_name).first()
            session.delete(delete)
            session.commit()
            return True
        except:
            return False
        
    def show_admins(self):
        try:
            select_admins = session.query(admins).all()
            admins_list = [
                {"user_name": admin.user_name,"password":admin.password, "traffic": admin.traffic, "inb_id": admin.inb_id}
                for admin in select_admins
            ]
            return admins_list
        except:
            False

    def add_chat_id(self, user_name, password, chat_id):
        try:
            check = check = session.query(admins).filter_by(user_name=user_name, password=password).all()
            if check:
                update = session.query(admins).filter(admins.user_name==user_name).update({'chat_id':chat_id})
                session.commit()
                return True
            else:
                return False
        except:
            False
    
    def remove_chat_id(self, chat_id):
        try:
            update = session.query(admins).filter(admins.chat_id==chat_id).update({'chat_id':None})
            session.commit()
            return True
        except:
            return False
        
    def admin_data(self, chat_id):
        try:
            get = session.query(admins).filter(admins.chat_id == chat_id).first()
            if not get:
                return False
            data = {
                "user_name": get.user_name,
                "traffic": get.traffic,
                "inb_id": get.inb_id
                }
            return data
        except:
            return False
        
    def reduce_traffic(self, chat_id, delta):
        try:
            admin_list = session.query(admins).filter(admins.chat_id==chat_id).all()
            if not admin_list:
                return False
            else:
                admin = admin_list[0]
                traffic = admin.traffic
                new_traffic = traffic + delta
                if new_traffic < 0:
                    new_traffic = 0
                session.query(admins).filter(admins.chat_id==chat_id).update({'traffic': new_traffic})
                session.commit()
                return True
        except:
            return False


        
    def admin_approval(self, chat_id):
        try:
            approv = session.query(admins).filter(admins.chat_id==chat_id).all()
            if approv:
                return True
            else:
                return False
        except:
            return False

admins_query = AdminsQuery()
# admins_query.add_admin('ali', 'ali', 1000, 8)
# admins_query.change_inb('ali', 2)
# admins_query.add_traffic('ali', 500).
# admins_query.delete_admin('mmd')
# admins_query.show_admins()
# admins_query.add_chat_id('ali', 'ali', 121111111)
# admins_query.remove_chat_id(121111111)
# get = admins_query.admin_data(121111111)
# if get:
#     print(get['traffic'])
# else:
#     print("No data found or an error occurred.")
# get_admin_traffic = admins_query.admin_data(121111111)
# admin_traffic = get_admin_traffic['traffic']
# print(admin_traffic)
# if admins_query.admin_approval(121111111):
#     print(1)
# else: print(2)
from log.logger_config import logger
import requests
import os
import json
from db.query import panels_query
from db.query import admins_query


class PanelAPI:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"Accept": "application/json"}
        self._current_panel = None

    def login(self, address, username, password):
        if self._current_panel == (address, username, password):
            return True

        try:
            url = f"https://{address}/login"
            data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(
                url, 
                data=data,
                headers=self.headers, 
                timeout=15
            )
            
            if response.status_code == 200:
                self._current_panel = (address, username, password)
                return True
            else:
                logger.error(f"Login failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def _make_request(self, method, url, **kwargs):
        address = kwargs.pop('address', '')
        username = kwargs.pop('username', '')
        password = kwargs.pop('password', '')
        
        try:
            if self._current_panel != (address, username, password):
                if not self.login(address, username, password):
                    return None

            response = method(url, **kwargs)
            
            if response.status_code in [401, 403]:
                if self.login(address, username, password):
                    response = method(url, **kwargs)
                else:
                    return None
            
            return response
            
        except Exception as e:
            logger.error(f"Error making {method.__name__} request to {url}: {e}")
            return None

    def add_user(self, chat_id, c_uuid, email, bytes_value, expiry_time, sub_id, inb_id):
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/inbound/addClient"
        settings = {
            "clients": [{
                "id": c_uuid,
                "enable": True,
                "flow": "",
                "email": email,
                "imitIp": "",
                "totalGB": bytes_value,
                "expiryTime": expiry_time,
                "tgId": "",
                "subId": sub_id,
                "reset": "",
            }]
        }
        data = {"id": inb_id, "settings": json.dumps(settings)}
        return self._make_request(
            self.session.post, 
            url, 
            json=data, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def show_users(self, chat_id, inb_id):
        print("show_users")
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/get/{inb_id}"
        return self._make_request(
            self.session.get, 
            url, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def user_obj(self, chat_id, email):
        print("user_obj")
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/getClientTraffics/{email}"
        return self._make_request(
            self.session.get, 
            url, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def reset_traffic(self, chat_id, inb_id, email):
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
        return self._make_request(
            self.session.post, 
            url, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def get_inbound(self, chat_id, inb_id):
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/get/{inb_id}"
        return self._make_request(
            self.session.get, 
            url, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def update_email(self, chat_id, user_id, data):
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/updateClient/{user_id}"
        return self._make_request(
            self.session.post, 
            url, 
            json=data, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )

    def delete_user(self, chat_id, inb_id, user_id):
        panel_info = get_panel_info(chat_id)
        if not panel_info:
            return None
        url = f"https://{panel_info['address']}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
        return self._make_request(
            self.session.post, 
            url, 
            address=panel_info['address'], 
            username=panel_info['username'], 
            password=panel_info['password']
        )
    
    
def get_panel_info(chat_id):
    try:
        admin_data = admins_query.admin_data(chat_id)
        panel_id = admin_data["panel_id"]
        panel_data = panels_query.get_panel_data(panel_id)
        data = {
        "address": panel_data["address"],
        "username": panel_data["username"],
        "password": panel_data["password"],
        "sub": panel_data["sub"],
        }
        return data
    except Exception as e:
        logger.error(f"Error getting panel info: {e}")
        return None
    
    
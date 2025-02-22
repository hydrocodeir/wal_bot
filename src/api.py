from config import PANEL_ADDRES, SUB_ADDRES
from log.logger_config import logger
import requests
import os
import json
from functools import wraps

class PanelAPI:
    def __init__(self):
        self.panel = PANEL_ADDRES
        self.session = requests.Session()
        self.headers = {"Accept": "application/json"}
        self.login()

    def login(self):
        try:
            url = f"https://{self.panel}/login"
            data = {"username": os.getenv("PANEL_USER"), "password": os.getenv("PANEL_PASS")}
            response = self.session.post(url, json=data, headers=self.headers, timeout=15)
            if response.status_code == 200:
                token = response.json().get("token")
                self.session.headers.update({"Authorization": f"Bearer {token}"})
            else:
                logger.error("Login failed! Check .env and your panel file.")
        except Exception as e:
            logger.error(f"Error during login: {e}")

    def ensure_logged_in(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
                if response.status_code == 401:
                    self.login()
                    response = func(self, *args, **kwargs)
                return response
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                return None
        return wrapper

    @ensure_logged_in
    def add_user(self, c_uuid, email, bytes_value, expiry_time, sub_id, inb_id):
        try:
            url = f"https://{self.panel}/panel/inbound/addClient"
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
            res = self.session.post(url, json=data)
            if res:
                return res
            else:
                logger.warning(f"Failed to add user {email}, response: {res.status_code}, message: {res.text}")
                return res.text
        except Exception as e:
            logger.error(f"Error in add_user: {e}")
            return None

    @ensure_logged_in
    def show_users(self, inb_id):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
            res = self.session.get(url)
            return res
        except Exception as e:
            logger.error(f"Error in show_users: {e}")
            return None

    @ensure_logged_in
    def user_obj(self, email):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/getClientTraffics/{email}"
            res = self.session.get(url)
            return res
        except Exception as e:
            logger.error(f"Error in user_obj: {e}")
            return None

    @ensure_logged_in
    def reset_traffic(self, inb_id, email):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
            res = self.session.post(url)
            return res
        except Exception as e:
            logger.error(f"Error in reset_traffic: {e}")
            return None

    @ensure_logged_in
    def get_inbound(self, inb_id):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
            res = self.session.get(url)
            return res
        except Exception as e:
            logger.error(f"Error in get_inbound: {e}")
            return None

    @ensure_logged_in
    def update_email(self, user_id, data):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/updateClient/{user_id}"
            res = self.session.post(url, json=data)
            return res
        except Exception as e:
            logger.error(f"Error in update_email: {e}")
            return None

    @ensure_logged_in
    def delete_user(self, inb_id, user_id):
        try:
            url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
            res = self.session.post(url)
            return res
        except Exception as e:
            logger.error(f"Error in delete_user: {e}")
            return None

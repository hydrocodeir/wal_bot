from config import PANEL_ADDRES
from log.logger_config import logger
import requests
import os
import json

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

    def _make_request(self, method, url, **kwargs):
        self.login()
        try:
            response = method(url, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Error making {method.__name__} request to {url}: {e}")
            return None

    def add_user(self, c_uuid, email, bytes_value, expiry_time, sub_id, inb_id):
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
        return self._make_request(self.session.post, url, json=data)

    def show_users(self, inb_id):
        url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
        return self._make_request(self.session.get, url)

    def user_obj(self, email):
        url = f"https://{self.panel}/panel/api/inbounds/getClientTraffics/{email}"
        return self._make_request(self.session.get, url)

    def reset_traffic(self, inb_id, email):
        url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
        return self._make_request(self.session.post, url)

    def get_inbound(self, inb_id):
        url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
        return self._make_request(self.session.get, url)

    def update_email(self, user_id, data):
        url = f"https://{self.panel}/panel/api/inbounds/updateClient/{user_id}"
        return self._make_request(self.session.post, url, json=data)

    def delete_user(self, inb_id, user_id):
        url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
        return self._make_request(self.session.post, url)
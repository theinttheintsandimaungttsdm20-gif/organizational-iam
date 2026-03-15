import requests 
from django.conf import settings


class IAMClient:
    @staticmethod
    def _headers(token):
        return {"Authorization": f"Bearer {token}"}
    # ===== LOGIN =====

    @staticmethod
    def login(email, password):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/auth/login/"
        return requests.post(url, json={"email": email, "password": password},)

    # ===== APPLICATIONS =====
    @staticmethod
    def get_applications(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/"
        return requests.get(url, headers=IAMClient._headers(token))

    @staticmethod
    def create_application(token, name, client_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/"
        return requests.post(url, json={"name": name, "client_id": client_id},
                             headers=IAMClient._headers(token))

    @staticmethod 
    def delete_application(token, app_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/{app_id}/"
        return requests.delete(url, headers=IAMClient._headers(token))

    # ===== EMPLOYEES =====    
    @staticmethod    
    def get_employees(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/"
        return requests.get(url, headers=IAMClient._headers(token))

    # ===== ROLES =====    
    @staticmethod    
    def get_roles(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/roles/"
        return requests.get(url, headers=IAMClient._headers(token))

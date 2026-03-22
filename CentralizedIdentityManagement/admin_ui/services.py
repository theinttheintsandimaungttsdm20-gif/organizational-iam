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
    
    @staticmethod
    def create_role(token, name):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/roles/"
        return requests.post(url, json={"name": name}, headers=IAMClient._headers(token))
    
    @staticmethod 
    def delete_role(token, role_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/roles/{role_id}/"
        return requests.delete(url, headers=IAMClient._headers(token))
    
    # ===== Scopes =====    
    @staticmethod    
    def get_scopes(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/scopes/"
        return requests.get(url, headers=IAMClient._headers(token))
    
    @staticmethod
    def create_scope(token, name, description):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/scopes/"
        return requests.post(url, json={"name": name, "description": description}, headers=IAMClient._headers(token))
    
    @staticmethod 
    def delete_scope(token, scope_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/scopes/{scope_id}/"
        return requests.delete(url, headers=IAMClient._headers(token))
    
    ## Role-Scope application resource restriction management
    @staticmethod
    def get_role_scopes(token, application_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/{application_id}/role-scopes/"
        return requests.get(url, headers=IAMClient._headers(token))

    @staticmethod
    def get_app_session_policy(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/session-policies/"
        return requests.get(url, headers=IAMClient._headers(token))
    
    @staticmethod
    def update_session_policy(token, application, timeout):
        print("Session Timeout Value: ", timeout)
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/session-policy/"
        payload = {
        "application": application,
        "session_timeout_seconds": timeout
        }
        return requests.put(url, json=payload, headers=IAMClient._headers(token))
    
    @staticmethod
    def update_role_scopes(token, payload):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/role-scopes/"
        return requests.put(url, json=payload, headers=IAMClient._headers(token))

    @staticmethod
    def delete_role_scope(token, rs_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/applications/role-scopes/{rs_id}/"
        return requests.delete(url, headers=IAMClient._headers(token))

    ## Employee Profile Management
    @staticmethod
    def create_employee(token, name, email, contact_number, title, department, join_date, role_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/"
        return requests.post(url, json={"name": name, "email": email, "contact_number": contact_number, "title": title,
                                        "department": department,  "join_date": join_date,  "role": role_id, },
                            headers=IAMClient._headers(token))


    @staticmethod
    def get_employees(token):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/"
        return requests.get(url, headers=IAMClient._headers(token))

    @staticmethod
    def get_employee(token, emp_id):
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/{emp_id}/"
        return requests.get(url, headers=IAMClient._headers(token))

    @staticmethod
    def update_employee(token, emp_id, name, email, contact_number, title, department, join_date, role_id):
        print("In Update Employee Service")
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/{emp_id}/"
        return requests.put(url, json={"name": name, "email" : email, "contact_number": contact_number, "title": title,
                                    "department": department, "join_date": join_date, "role": role_id, },
                            headers=IAMClient._headers(token))

    @staticmethod
    def delete_employee(token, emp_id):
        print("In Delete Employee Service")
        url = f"{settings.IAM_API_BASE_URL}/api/admin/employees/delete/{emp_id}/"
        return requests.delete(url, headers=IAMClient._headers(token))

    
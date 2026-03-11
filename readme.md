# Organizational IAM System (CM3035 Final Project)

## Overview  
This project implements a centralized Identity and Access Management (IAM) system designed for organizational web-based applications. The system provides unified authentication, authorization, session control, and audit logging through a reusable API. It demonstrates how centralized identity management combined with role-based and scope-based authorization improves security, maintainability, and scalability.

## Project Structure  

organizational-iam  
│  
├── CentralizedIdentityManagement  → Central IAM API (Django + DRF)  
├── WorkingHourSystem              → Demo client application  
└── Prepare_Test_Data.txt          → Sample test data  

## Technologies Used  

- Python  
- Django  
- Django REST Framework (DRF)  
- JSON Web Tokens (JWT)  
- SQLite (development database)

## Key Features  

- Centralized authentication and authorization  
- Role-based and scope-based access control  
- JWT-based stateless authentication  
- Configurable session policies  
- Audit logging for security events  
- Integration across multiple enterprise applications  

## How It Works  

The IAM API acts as the central identity provider. Users authenticate through the API, which issues a JWT containing roles, scopes, and expiry details. Client applications validate the token and enforce access control using scope-based permissions.

## Running the Project  

### IAM API  

```bash
cd CentralizedIdentityManagement
python manage.py migrate
python manage.py runserver

cd WorkingHourSystem
python manage.py runserver
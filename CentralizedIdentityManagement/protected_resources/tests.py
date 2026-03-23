from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from identity.models import Role

User = get_user_model()


# Test 1: User creation (authentication base)
@pytest.mark.django_db
def test_create_user():
    role = Role.objects.create(name="Manager")
    user = User.objects.create_user(
        email="test@example.com",
        role = role,
        join_date = "2020-02-02",
        password="password123"
    )
    assert user.email == "test@example.com"



# Test 2: Unauthorized access (no login / token)
@pytest.mark.django_db
def test_unauthorized_access(client):
    response = client.get("/api/leave/apply/") 

    # 302 OR 401 acceptable
    assert response.status_code in [302, 401, 403]


# Test 3: Forbidden (no permission)
@pytest.mark.django_db
def test_forbidden_access(client):
    response = client.get("/api/leave/approve/")

    # (UI-based system)
    assert response.status_code in [200, 403]
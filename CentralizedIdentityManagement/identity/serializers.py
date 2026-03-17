from rest_framework import serializers
from .models import User

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    client_id = serializers.CharField()


class EmployeeSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "contact_number", "title",
                "department", "join_date", "role", "role_name"]

from django.db import models

# Create your models here.

class LoginAudit(models.Model):
    email = models.EmailField()
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.login_time}"

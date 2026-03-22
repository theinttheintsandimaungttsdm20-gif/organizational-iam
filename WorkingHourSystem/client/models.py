from django.db import models

# Create your models here.
class Report(models.Model):
    user_email = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
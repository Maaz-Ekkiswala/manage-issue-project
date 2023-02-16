from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.
class UserProfile(User):
    avatar = models.ImageField(upload_to='avatars/', null=True, default=None)
    mobile = models.CharField(max_length=10, unique=True, verbose_name="mobile number")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_profile"

    def clean_fields(self, exclude=None):
        try:
            mobile = int(self.mobile)
            if len(mobile) != 10:
                raise ValidationError("Mobile should have exactly 10 digits")
        except:
            raise ValidationError({"mobile_number": "Enter valid mobile number."})
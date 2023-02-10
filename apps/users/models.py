from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.
class UserProfile(User):
    avatar = models.ImageField(upload_to='avatars/', null=True, default=None)
    mobile = models.CharField(max_length=10, unique=True, verbose_name="mobile number")

    EMAIL_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_profile"

    def clean_fields(self, exclude=None):
        try:
            int(self.mobile)
            if len(self.mobile) != 10:
                raise ValidationError("")
        except:
            raise ValidationError({"mobile_number": "Enter valid mobile number."})
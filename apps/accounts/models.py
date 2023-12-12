from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# カスタム定義のユーザ（社員番号, パスワード, 氏名）
class CustomUserManager(BaseUserManager):
    def create_user(self, employee_number, full_name, password=None):
        if not employee_number:
            raise ValueError('The Employee number must be set')
        user = self.model(employee_number=employee_number, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_number, full_name, password=None):
        user = self.create_user(employee_number, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 社員番号（正規表現で6桁の数字に限定している）
    employee_number = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$')],
        unique=True,
        primary_key=True,
    )
    # 氏名
    full_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'employee_number'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.employee_number
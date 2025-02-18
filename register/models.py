import random
import string



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class FoydalanuvchiUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email manzili ko'rsatilishi shart!")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser uchun 'is_staff=True' bo'lishi shart!")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser uchun 'is_superuser=True' bo'lishi shart!")

        return self.create_user(email, password, **extra_fields)


class Foydalanuvchi(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    objects = FoydalanuvchiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Hech narsa kiritilmagan

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(Foydalanuvchi, on_delete=models.CASCADE, related_name='profile')  # 'register.Foydalanuvchi' o'rniga 'Foydalanuvchi' ishlatildi
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"



    #####################################################################################################################
    # doctor
    #
    #
    # class UserManager(BaseUserManager):
    #     def create_user(self, email, first_name, last_name, passport_id, verification_code=None, is_verified=False):
    #         if not email:
    #             raise ValueError("Email kiritish shart")
    #         email = self.normalize_email(email)
    #         user = self.model(
    #             email=email,
    #             first_name=first_name,
    #             last_name=last_name,
    #             passport_id=passport_id,
    #             verification_code=verification_code or self.generate_verification_code(),
    #             is_verified=is_verified
    #         )
    #         user.save(using=self._db)
    #





class DoctorRegisterManager(BaseUserManager):
    def create_user(self, email, name, surname, passport_id, verification_code=None, is_verified=False):
        if not email:
            raise ValueError("Email kiritish shart")
        email = self.normalize_email(email)
        doctor = DoctorRegister(
            email=email,
            name=name,
            surname=surname,
            passport_id=passport_id,
            verification_code=verification_code or self.generate_verification_code(),
            is_verified=is_verified
        )
        doctor.save(using=self._db)

        # Profile yaratish
        Profile.objects.create(user=doctor)
        return doctor

    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))


class DoctorRegister(AbstractBaseUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    passport_id = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Faqat tibbiy maslahat bera olish uchun
    is_superuser = models.BooleanField(default=False)  # Bu xususiyatni faqat admin uchun qoldiring

    objects = DoctorRegisterManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'passport_id']

    def __str__(self):
        return self.email


class DoctorProfile(models.Model):
    user = models.OneToOneField(DoctorRegister, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"


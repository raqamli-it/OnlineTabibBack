from django.core.mail import send_mail
from tutorial.quickstart.serializers import UserSerializer

from .models import  Profile


from rest_framework import serializers
from .models import Foydalanuvchi

# Foydalanuvchi ro'yxatga olish serializeri
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'name', 'surname']

    def create(self, validated_data):
        # Yangi foydalanuvchi yaratish
        user = Foydalanuvchi.objects.create_user(**validated_data)
        user.is_active = False  # Foydalanuvchi tasdiqlanmaguncha faol emas
        user.save()
        return user


# Emailni tasdiqlash serializeri
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

# Email orqali kirish uchun serializer
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Login uchun tasdiqlash kodi serializeri
class VerifyLoginCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6)

# Foydalanuvchi profilini olish uchun serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'avatar', 'is_email_verified']
        read_only_fields = ['email', 'is_email_verified']



####################################################################################################################
#doctor

class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'name', 'surname', 'passport_id']

    def create(self, validated_data):
        user = Foydalanuvchi.objects.create_user(**validated_data)
        send_mail(
            "Tasdiqlash Kodingiz",
            f"Sizning tasdiqlash kodingiz: {user.verification_code}",
            "noreply@example.com",
            [user.email],
            fail_silently=False
        )
        return user

class Verify_EmailSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'email', 'name', 'surname')
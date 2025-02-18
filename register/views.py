
from rest_framework import status, permissions, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import get_user_model
import random
import string

from .models import Foydalanuvchi, DoctorRegister, Profile
from .serializers import RegisterSerializer, VerifyEmailSerializer, EmailLoginSerializer, VerifyLoginCodeSerializer, \
    UserProfileSerializer, LoginSerializer
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

# Ro'yxatdan o'tish view
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Tasdiqlash kodi yaratish
            verification_code = ''.join(random.choices(string.digits, k=6))
            user.verification_code = verification_code
            user.save()

            # Emailga tasdiqlash kodi yuborish
            send_mail(
                'Tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {verification_code}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            return Response({
                "message": "Ro'yxatdan o'tdingiz. Emailga tasdiqlash kodi yuborildi."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Emailni tasdiqlash view
class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']

            try:
                user = Foydalanuvchi.objects.get(email=email)
                if user.verification_code == verification_code:
                    user.is_email_verified = True
                    user.is_active = True  # Tasdiqlangach faol bo'ladi
                    user.verification_code = None  # Kodni o'chirish
                    user.save()
                    return Response({"message": "Email tasdiqlandi!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Tasdiqlash kodi noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)
            except Foydalanuvchi.DoesNotExist:
                return Response({"message": "Foydalanuvchi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login view
class LoginView(APIView):
    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)

                # Tasdiqlash kodi yaratish
                verification_code = ''.join(random.choices(string.digits, k=6))
                user.verification_code = verification_code
                user.save()

                # Emailga tasdiqlash kodini yuborish
                send_mail(
                    'Kirish uchun tasdiqlash kodi',
                    f'Sizning tasdiqlash kodingiz: {verification_code}',
                    'no-reply@yourdomain.com',
                    [user.email],
                    fail_silently=False,
                )

                return Response({
                    "message": "Tasdiqlash kodi emailga yuborildi."
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"message": "Email ro'yxatdan o'tmagan!"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login uchun tasdiqlash kodi view
class VerifyLoginCodeView(APIView):
    def post(self, request):
        serializer = VerifyLoginCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']

            try:
                user = User.objects.get(email=email)

                if user.verification_code == verification_code:
                    user.verification_code = None  # Kodni o‘chirish
                    user.save()

                    # JWT token yaratish
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                        'access_token': access_token,
                        'refresh_token': str(refresh),
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({"message": "Tasdiqlash kodi noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response({"message": "Foydalanuvchi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Tizimdan chiqish view
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Agar foydalanuvchi superuser bo'lsa, logout qilinmaydi
            if request.user.is_superuser:
                return Response({"message": "Superuser tizimdan chiqmaydi!"}, status=status.HTTP_403_FORBIDDEN)

            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"message": "Refresh token taqdim etilmadi."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Tokenni qora ro‘yxatga kiritish (bloklash)

            return Response({"message": "Muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "Xatolik yuz berdi.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Foydalanuvchi profilini ko'rish va yangilash view
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Avatarni yuklash uchun view
class UploadAvatarView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user


##############################################################################################################################################################
#doctor

class DoctorRegisterView(APIView):
    """
    Register a doctor.
    A verification code is sent to the email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                "Verification Code",
                f"Your verification code is: {user.verification_code}",
                "noreply@example.com",
                [user.email],
                fail_silently=False
            )
            return Response({"message": "Verification code sent to email!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Verify_EmailView(APIView):
    """
    Email verification.
    The doctor provides the email and verification code.
    If correct, the account is activated.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            verification_code = serializer.validated_data["verification_code"]
            user = DoctorRegister.objects.filter(email=email, verification_code=verification_code).first()

            if user:
                user.is_verified = True
                user.verification_code = None
                user.save()
                return Response({"message": "Verification successful!"}, status=status.HTTP_200_OK)

            return Response({"error": "Incorrect code"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLoginView(APIView):
    """
    Log in a doctor.
    If the email is verified, an access token is returned.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = DoctorRegister.objects.filter(email=email, is_verified=True).first()

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Logged in successfully!",
                    "token": token.key
                }, status=status.HTTP_200_OK)

            return Response({"error": "Email not verified or incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLogoutView(APIView):
    """
    Log out the doctor.
    The doctor logs out using the access token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Delete the token to log out
        return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            doctor = DoctorRegister.objects.get(email=request.user.email)  # Use email to get the doctor
            profile = Profile.objects.filter(user=doctor).first()  # Get the profile as well

            data = {
                "name": doctor.name,
                "surname": doctor.surname,
                "email": doctor.email,
                "passport_id": doctor.passport_id,
                "avatar": profile.avatar.url if profile and profile.avatar else None
            }
            return Response(data, status=200)
        except DoctorRegister.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=404)
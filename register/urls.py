from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RegisterView, VerifyEmailView, LoginView, UserProfileView, UploadAvatarView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    ##############
    path("doctor_register/", RegisterView.as_view(), name="register"),
    path("verify_email/", VerifyEmailView.as_view(), name="verify-email"),
    path("doctor_login/", LoginView.as_view(), name="login"),
    path("doctor_logout/", LogoutView.as_view(), name="logout"),
    path('doctor_profile/', ProfileView.as_view(), name='profile'),

]

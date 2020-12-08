from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import LoginView, LogoutView, RegisterationView, UsernameValidationView, EmailValidationView, VerificationView

urlpatterns = [
    path('register/', RegisterationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()),
         name="validate_username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()),
         name="validate_email"),
    path('activate/<uidb64>/<token>/',
         VerificationView.as_view(), name="activate"),
]

from django.urls import path
from .views import Register, ValidateUser, Deposit, Withdraw, SignUp


app_path = "atm_machine"

urlpatterns = [
    path('signUp/', SignUp.as_view()),
    path('register/', Register.as_view()),
     path('validateUser/', ValidateUser.as_view()),
     path('deposit/', Deposit.as_view()),
     path('withdraw/', Withdraw.as_view()),
 ]
from api.views import GetToken, SignUp
from django.urls import path

urlpatterns = [
    path('token/', GetToken.as_view()),
    path('signup/', SignUp.as_view()),

]

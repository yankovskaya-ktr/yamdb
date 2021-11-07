from django.urls import path

from api.views import GetToken, SignUp

urlpatterns = [
    path('token/', GetToken.as_view()),
    path('signup/', SignUp.as_view()),

]

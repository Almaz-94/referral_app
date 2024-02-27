from django.urls import path

from users_api.apps import UsersConfig
from users_api.views import UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, \
    UserLoginAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('signup/', UserCreateAPIView.as_view()),
    path('update/<int:pk>/', UserUpdateAPIView.as_view()),
    path('<int:pk>/', UserRetrieveAPIView.as_view()),
    path('token/', UserLoginAPIView.as_view()),

]
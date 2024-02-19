from django.urls import path

from users_api.apps import UsersConfig
from users_api.views import UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, MyTokenObtainPairView


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('update/<int:pk>/', UserUpdateAPIView.as_view()),
    path('<int:pk>/', UserRetrieveAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view())

]
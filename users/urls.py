from django.urls import path
from .views import user_list_create, AuthView, user_profile

urlpatterns = [
    path('users/', user_list_create, name='user-list-create'),
    path('user/auth/', AuthView.as_view(), name='user-auth'),
    path('profile/', user_profile, name='user-profile'),

]
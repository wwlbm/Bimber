from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, discover_view, rate_user, inbox_view, view_profile

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('discover/', discover_view, name='discover'),
    path('rate/<int:user_id>/<str:action>/', rate_user, name='rate_user'),
    path('inbox/', inbox_view, name='inbox'),
    path('view_profile/<int:user_id>/', view_profile, name='view_profile'),
]

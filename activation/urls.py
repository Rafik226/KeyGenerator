from django.urls import path
from . import views
from .views import CustomLoginView, generate_activation_code, activation_history, logout_view, signup_view

urlpatterns = [
    path('', views.welcome, name='welcome'),  # Page de bienvenue
    path('generate/', generate_activation_code, name='generate_activation_code'),  # Génération protégée par login
    path('login/', CustomLoginView.as_view(), name='login'),  # Page de connexion
    path('history/', activation_history, name='activation_history'),  # Historique
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),  # Déconnexion
]

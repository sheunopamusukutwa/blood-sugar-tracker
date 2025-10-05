from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ReadingListCreateView, ReadingDetailView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('readings/', ReadingListCreateView.as_view(), name='readings'),
    path('readings/<int:pk>/', ReadingDetailView.as_view(), name='reading-detail'),
]
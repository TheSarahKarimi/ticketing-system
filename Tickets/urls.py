from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:pk>/edit/', views.ticket_edit, name='ticket_edit'),
    path('ticket/<int:pk>/delete/', views.ticket_delete, name='ticket_delete'),
]
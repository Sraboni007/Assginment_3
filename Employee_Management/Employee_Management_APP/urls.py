# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.employee_list, name='home'), 
    path('add_employee/', views.add_employee, name='add_employee'),  
    path('update/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'), 
]

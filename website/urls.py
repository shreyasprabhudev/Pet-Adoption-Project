from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.adoptable_pets, name='adoptable_pets'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.user_record, name='record'),
    path('delete_pet/<int:pk>', views.delete_pet, name='delete_pet'),
    path('update_pet/<int:pk>', views.update_pet, name='update_pet'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('add_shelter/', views.add_shelter, name='add_shelter'),
]
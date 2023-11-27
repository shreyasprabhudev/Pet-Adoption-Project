from django.contrib import admin
from .models import UserInformation, Pet, Employee, Shelter

admin.site.register(UserInformation)
admin.site.register(Pet)
admin.site.register(Employee)
admin.site.register(Shelter)
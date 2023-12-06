from django.conf import settings
from django.db import models

class UserInformation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userinformation')

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    is_employee = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "UserInformation"

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

class Shelter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    shelter_name = models.CharField(max_length=50)
    shelter_email = models.CharField(max_length=100)
    shelter_phone = models.CharField(max_length=15)
    shelter_address = models.CharField(max_length=100)
    shelter_city = models.CharField(max_length=50)
    shelter_state = models.CharField(max_length=50)
    shelter_zipcode = models.CharField(max_length=20)
    shelter_employees_count = models.IntegerField(default=0)
    shelter_pets_count = models.IntegerField(default=0)

    def __str__(self):
        return(f"{self.shelter_name}")

class Pet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    pet_name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    fixed = models.BooleanField()
    pet_image = models.ImageField(null=True, blank=True, upload_to="images/")
    pet_shelter_id = models.ForeignKey(Shelter, on_delete=models.SET_NULL, related_name="pet", null=True)

    def __str__(self):
        return(f"{self.pet_name}")
    
class Employee(models.Model):
    employee_id = models.OneToOneField(UserInformation, on_delete=models.CASCADE, related_name="employee", primary_key=True)
    employee_shelter_id = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(default=0)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee, Pet, UserInformation, Shelter

@receiver(post_save, sender=Employee)
def update_employee_count_on_save(sender, instance, **kwargs):
    if instance.employee_shelter_id:
        employee_count = Employee.objects.filter(employee_shelter_id=instance.employee_shelter_id).count()
        instance.employee_shelter_id.shelter_employees_count = employee_count
        instance.employee_shelter_id.save()

@receiver(post_delete, sender=Employee)
def update_employee_count_on_delete(sender, instance, **kwargs):
    if instance.employee_shelter_id:
        employee_count = Employee.objects.filter(employee_shelter_id=instance.employee_shelter_id).count()
        instance.employee_shelter_id.shelter_employees_count = employee_count
        instance.employee_shelter_id.save()

@receiver(post_save, sender=Pet)
def update_pet_count_on_save(sender, instance, **kwargs):
   if instance.pet_shelter_id:
        shelter = instance.pet_shelter_id
        shelter.shelter_pets_count = Pet.objects.filter(pet_shelter_id=shelter).count()
        shelter.save()

@receiver(post_delete, sender=Pet)
def update_pet_count_on_delete(sender, instance, **kwargs):
    if instance.pet_shelter_id:
        shelter = instance.pet_shelter_id
        shelter.shelter_pets_count = Pet.objects.filter(pet_shelter_id=shelter).count()
        shelter.save()

@receiver(post_save, sender=UserInformation)
def create_employee_record(sender, instance, created, **kwargs):
    if instance.is_employee and (created or not Employee.objects.filter(employee_id=instance).exists()):
        default_shelter = Shelter.objects.first()

        if default_shelter:
            Employee.objects.create(employee_id=instance, employee_shelter_id=default_shelter)
        else:
            pass
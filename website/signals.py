from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee, Pet

@receiver(post_save, sender=Employee)
def update_employee_count_on_save(sender, instance, **kwargs):
    instance.shelter.shelter_employees_count = instance.shelter.employee.count()
    instance.shelter.save()

@receiver(post_delete, sender=Employee)
def update_employee_count_on_delete(sender, instance, **kwargs):
    instance.shelter.shelter_employees_count = instance.shelter.employee.count()
    instance.shelter.save()

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
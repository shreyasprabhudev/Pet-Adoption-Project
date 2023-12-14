from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddPetForm, AddShelterForm
from .models import UserInformation, Shelter, Pet

def home(request):
    if request.user.is_authenticated:
        return redirect('adoptable_pets')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('adoptable_pets')
        else:
            messages.error(request, "There was an error logging in!")
            return redirect('home')
    else:
        return render(request, 'home.html')
    
def adoptable_pets(request):
    pets = Pet.objects.all()
    breeds = Pet.objects.values_list('breed', flat=True).distinct()
    breed = request.GET.get('breed')
    age = request.GET.get('age')
    ages = Pet.objects.values_list('age', flat=True).distinct()
    sex = request.GET.get('sex')
    sexes = Pet.objects.values_list('sex', flat=True).distinct()
    shelter_id = request.GET.get('shelter')
    shelters = Shelter.objects.all()

    if breed:
        pets = pets.filter(breed=breed)
    if age:
        pets = pets.filter(age=age)
    if sex:
        pets = pets.filter(sex=sex)
    if shelter_id:
        pets = pets.filter(pet_shelter_id=shelter_id)

    if request.user.is_authenticated:
        data = {
            'pets': pets,
            'breeds': breeds,
            'ages': ages,
            'sexes': sexes,
            'shelters': shelters,
        }
        return render(request, 'adoptable_pets.html', data)
    else:
        messages.success(request, "You Must Be Logged In!")
        return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')

def register_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You Are Already Logged In!")
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_info = UserInformation(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode'],
            )

            user_info.save()

            login(request, user)

            messages.success(request, "You Have Successfully Registered!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def add_pet(request):
    if request.user.is_authenticated:
        user_info = UserInformation.objects.get(user=request.user)
        if user_info.is_employee:
            if request.method == "POST":
                form = AddPetForm(request.POST or None, request.FILES)
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Pet Added!")
                    return redirect('home')
            else:
                form = AddPetForm()
            return render(request, 'add_pet.html', {'form': form})
    else:
        messages.success(request, "Access Denied: You Must Be An Employee!")
        return redirect('home')
    
def add_shelter(request):
    if request.user.is_authenticated:
        user_info = UserInformation.objects.get(user=request.user)
        if user_info.is_employee:
            if request.method == "POST":
                form = AddShelterForm(request.POST or None, request.FILES)
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Shelter Added!")
                    return redirect('home')
            else:
                form = AddShelterForm()
            return render(request, 'add_shelter.html', {'form': form})
    else:
        messages.success(request, "Access Denied: You Must Be An Employee!")
        return redirect('home')

def user_record(request, pk):
    if request.user.is_authenticated:
        user_record = UserInformation.objects.get(id=pk)
        return render(request, 'record.html', {'user_record': user_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
def delete_pet(request, pk):
    if request.user.is_authenticated:
        user_info = UserInformation.objects.get(user=request.user)
        if user_info.is_employee:
            pet_to_delete = get_object_or_404(Pet, pk=pk)
            pet_to_delete.delete()
            messages.success(request, "Pet Record Deleted Successfully!")
            return redirect('adoptable_pets')
        else:
            messages.error(request, "Access Denied: You Must Be An Employee!")
            return redirect('home')
    else:
        messages.error(request, "You Must Be Logged In!")
        return redirect('home')
    
def update_pet(request, pk):
    if request.user.is_authenticated:
        try:
            user_info = UserInformation.objects.get(user=request.user)
        except UserInformation.DoesNotExist:
            messages.error(request, "User information not found. Please complete your profile.")
            return redirect('home')

        if user_info.is_employee:
            current_pet = get_object_or_404(Pet, pk=pk)
            if request.method == "POST":
                form = AddPetForm(request.POST, request.FILES, instance=current_pet)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Pet Information Has Been Updated!")
                    return redirect('adoptable_pets')
            else:
                form = AddPetForm(instance=current_pet)
            return render(request, 'update_pet.html', {'form': form, 'pet': current_pet})
        else:
            messages.error(request, "Access Denied: You Must Be An Employee!")
            return redirect('home')
    else:
        messages.error(request, "You Must Be Logged In!")
        return redirect('home')
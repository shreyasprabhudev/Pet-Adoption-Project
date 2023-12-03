from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import UserInformation, Shelter, Pet, Employee

def home(request):
    records = UserInformation.objects.all()
    shelters = Shelter.objects.all()
    pets = Pet.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an error!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records, 'shelters': shelters, 'pets': pets})
    
def adoptable_pets(request):
    pets = Pet.objects.all()

    if request.user.is_authenticated:
        return render(request, 'adoptable_pets.html', {'pets': pets})
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            user_info = UserInformation(
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


            messages.success(request, "You Have Successfully Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})

def user_record(request, pk):
    if request.user.is_authenticated:
        user_record = UserInformation.objects.get(id=pk)
        return render(request, 'record.html', {'user_record': user_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete = UserInformation.objects.get(id=pk)
        delete.delete()
        messages.success(request, "Record Deleted Successfully!")
        return redirect('home')
    else:
        messages.success(request, "You Need To Be Logged In To Delete!")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None, request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In!")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = UserInformation.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In!")
        return redirect('home')
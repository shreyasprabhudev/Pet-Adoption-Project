from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserInformation, Pet, Shelter

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label="", max_length=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    zipcode = forms.IntegerField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
    password2 = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'state', 'zipcode', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>150 characters max with letters, digits, and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

class AddUserInformationForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    last_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    email = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}), label="")
    address = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")
    city = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "City", "class": "form-control"}), label="")
    state = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "State", "class": "form-control"}), label="")
    zipcode = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}), label="")

    class Meta:
        model = UserInformation
        exclude = ("is_employee",)

class AddPetForm(forms.ModelForm):
    pet_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Pet Name", "class": "form-control"}), label="")
    breed = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Breed", "class": "form-control"}), label="")
    sex = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Sex", "class": "form-control"}), label="")
    age = forms.IntegerField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}))
    fixed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    pet_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    pet_shelter_id = forms.ModelChoiceField(queryset=Shelter.objects.all(), widget=forms.Select(attrs={"class": "form-select"}), empty_label="Select Shelter")

    class Meta:
        model = Pet
        fields = ['pet_name', 'breed', 'sex', 'age', 'fixed', 'pet_image', 'pet_shelter_id']

    def clean_pet_image(self):
        pet_image = self.cleaned_data.get('pet_image')
        return pet_image
    
class AddShelterForm(forms.ModelForm):
    shelter_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Shelter Name", "class": "form-control"}), label="")
    shelter_email = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Shelter Email", "class": "form-control"}), label="")
    shelter_phone = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Shelter Phone", "class": "form-control"}), label="")
    address = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")
    city = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "City", "class": "form-control"}), label="")
    state = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "State", "class": "form-control"}), label="")
    zipcode = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}), label="")

    class Meta:
        model = Shelter
        fields = ['shelter_name', 'shelter_email', 'shelter_phone', 'address', 'city', 'state', 'zipcode']
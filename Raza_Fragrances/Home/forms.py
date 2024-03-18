from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from accounts.models import User
from .models import Customer_Details, Review


# Sign up Form
class signupForm(UserCreationForm):
    first_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'Ec-input mt-3 position-relative pb-1','placeholder':'Full Name', 'autofocus':True}), error_messages={'required':"Full name is required."})

    email = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'Ec-input mt-3 position-relative pb-1','placeholder':'Email address'}), error_messages={'required':"Email is required."})

    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'Ec-input mt-3 position-relative pb-1','placeholder':'Password'}), error_messages={'required':"Password is required."})

    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'Ec-input mt-3 position-relative pb-1','placeholder':'Confirm Password'}), error_messages={'required':"Confirm password is required."})
    
    class Meta(UserChangeForm):
        model = User
        fields = ['first_name', 'email']



# Login Form   
class loginForm(AuthenticationForm):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'Ec-input mt-3 position-relative pb-1','placeholder':'Email address', 'autofocus':True}), error_messages={'required':"Please enter your email."})
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'Ec-input mt-5 position-relative pb-1','placeholder':'Password'}), error_messages={'required':"Please enter your password."} )


# This is for Profile of a user
class User_Profile(UserChangeForm):
    password = None

    date_joined = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2 w-100'}), disabled=True)

    last_login = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-2'}), disabled=True)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'Ec-Profile-input mt-2'}), required=True ,error_messages={'required':'Please Enter Your First Name.'})

    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'Ec-Profile-input mt-2'}), required=True,error_messages={'required':'Please Enter Your Email address.'})

    class Meta(UserChangeForm):
        model = User
        fields = ['email', 'first_name', 'date_joined', 'last_login']


# Add New Address class
class NewAddress(forms.ModelForm):
    
    Name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'mt-3','placeholder':'Full Name','autofocus':True}), required=True, error_messages={'required':"Please fill out You'r Full Name."})

    Mobile_Number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'mt-3','placeholder':'Mobile Number'}),required=True, error_messages={'required':'Please fill out Mobile Number.'})

    Pincode = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':'mt-3','placeholder':'Pincode'}), required=True, error_messages={'required':'Please Enter a Pincode.'})

    City = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':'mt-3','placeholder':'City / District / Town'}), required=True, error_messages={'required':'Please Enter Your City / Town / District.'})

    Address = forms.CharField(label='', widget=forms.Textarea(attrs = {'placeholder':'Address (Area and Street)', 'rows':'3'}), required=True, error_messages={'required':'Please fill out Your Address.'})

    Landmark = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':'mt-3','placeholder':'Landmark'}), required=True, error_messages={'required':"Please fill out Landmark."})

    class Meta:
        model = Customer_Details
        fields  = ['Name', 'Mobile_Number', 'Pincode', 'City', 'Address', 'State', 'Landmark']


# This is for Change Password
class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pb-2' ,'placeholder':'Old Password','autofocus':True}), error_messages={'required':"Please Enter your old password."})

    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pb-2' ,'placeholder':'New Password'}), error_messages={'required':"Please enter new password."})

    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pb-2' ,'placeholder':'New Password (Confirmation)'}), error_messages={'required':"Please confirm new password."})


# This if for Reset password
class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='' ,max_length = 250, widget=forms.TextInput(attrs={'class':'Ec-input', 'placeholder':'Email address'}))


# for Reset password.
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='', max_length=250, widget=forms.PasswordInput(attrs={'class':'Ec-input', 'placeholder':'Password'}))
    new_password2 = forms.CharField(label='', max_length=250, widget=forms.PasswordInput(attrs={'class':'Ec-input', 'placeholder':'Confirm Password'}))
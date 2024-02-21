from django import forms
from accounts.models import MyUser

class UserSignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=156, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = MyUser
        fields = ("username","email","phone","full_name")

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user
    
    

# class ProfileForm(forms.ModelForm):
    
#     phone = PhoneNumberField()
#     full_name = forms.CharField(max_length=50)
    
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['phone'].initial = user.phone
#             self.fields['full_name'].initial = user.full_name
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})
#             self.fields[field].widget.attrs.update({'style': 'width: 350px;'})
#         # Set email field as read-only

#     class Meta:
#         model = Profile
#         fields = ['phone','full_name','bio','profile_picture']
        
        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    # phone = PhoneNumberField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'style': 'width: 350px;'})

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("New password and Confirm password do not match!")

        return cleaned_data
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Name", max_length=150)
    last_name = forms.CharField(label="Surname", max_length=150)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=20)
    address = forms.CharField(label="Address", widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "address", "password1", "password2"]
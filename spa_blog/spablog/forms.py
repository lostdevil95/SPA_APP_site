from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Comment


class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "InputUsername",
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "InputPassword",
        }),
    )
    repeat_password = forms.CharField(required=True,
                                      widget=forms.PasswordInput(attrs={
                                          'class': "form-control",
                                          'id': "ReInputPassword",
                                      }),
                                      )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']
        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
        validate_password(password)

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):

    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': "form-control",
                                   'id': "InputUsername", }),
                               )

    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': "form-control",
                                   'id': "InputUsername", }),
                               )


class ContactForm(forms.Form):
    name = forms.CharField( max_length=100,
        required=True)

    email = forms.CharField( max_length=50,
        required=True)

    subject = forms.CharField( max_length=100,
        required=True)

    message = forms.CharField( max_length=1000,
        required=True)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widget = forms.Textarea(attrs={'class': 'form-control',
                                       'row': 3})
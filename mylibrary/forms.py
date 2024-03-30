from django import forms
from .models import Comment, Book, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['book','theme', 'nickname', 'text']

        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': 'Здоровое питание'}),
            'text': forms.Textarea(attrs={'placeholder': 'Хочу рассказать о...'})
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'picture', 'author', 'description', 'pages', 'price', 'type_cover', 'size', 'date_public','category', 'exist']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Придумайте пароль')
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2', ]

class ContactUsForm(forms.Form):
    subject = forms.CharField(
        label='Тема сообщения:',
    )
    sender = forms.EmailField(
        label='Ваш e-mail:',
        widget=forms.EmailInput()
    )

    content = forms.CharField(
        label='Сообщение:',
        widget=forms.Textarea(
            attrs={'rows': 11, }
        )
    )

from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Ім'я студента",
                               widget=forms.TextInput(attrs={
                                   "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={
                                   "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))

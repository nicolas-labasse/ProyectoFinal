
from urllib import request
from urllib.request import Request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ProyectoFinalApp.models import *
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput) 
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FormArticulo(forms.ModelForm):
    #titulo = forms.CharField(max_length=50)
    #subTitulo = forms.CharField(max_length=50)
    #contenido = forms.CharField(max_length=500,widget=forms.Textarea)
    #autor = forms.CharField( max_length=50)
    #imagen = forms.ImageField(label="Imagen",required=False)
    #fecha_creacion =  forms.DateTimeField(initial="")

    class Meta:
        model = articulo
        fields = ['titulo', 'subTitulo', 'contenido', 'autor', 'imagen']

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Imagen", required=False)

    class Meta:
        model = Avatar
        fields = ['imagen']
        
class UserEditForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class FormMensaje(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['usuario_receptor', 'mensaje']



class LinkForm(forms.Form):
    link1 = forms.URLField(label="",required=False,)
    link2 = forms.URLField(label="",required=False)
    class Meta:
        model = Link
        fields = ['link1', 'link2']
from genericpath import exists
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render

from ProyectoFinalApp.forms import *

from ProyectoFinalApp.models import *

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages




def inicio(request):
    url = "/media/imagenes/4.jpg"
    url_nosotros = "/media/imagenes/5.jpg"
    url_blog = "/media/imagenes/6.jpg"
    tab = "inicio"
    return render(request, 'ProyectoFinalApp/index.html', {'url':url, 'url_nosotros':url_nosotros, 'url_blog':url_blog, 'tab':tab})

def nosotros(request):
    url = "/media/imagenes/3.jpg"
    url_integrante = "/media/imagenes/80.jpg"
    tab = "nosotros"
    return render(request, 'ProyectoFinalApp/about.html', {'url':url, 'url_integrante':url_integrante, 'tab':tab})

def pages(request):
    tab = "pages"
    page = request.GET.get('page', 1)
    buscar = request.GET.get('buscar')
    if buscar is not None and buscar is not "":
        buscador = articulo.objects.filter( Q(titulo__icontains=buscar) | Q(autor__icontains=buscar))
        paginator = Paginator(buscador, 6)
        buscador = paginator.page(page)
        return render(request,"ProyectoFinalApp/pages.html",{'buscador':buscador,'buscar':buscar,'paginator':paginator,'tab':tab})
    else:
        articulos = articulo.objects.all().order_by('-id')
        paginator = Paginator(articulos, 6)
        articulos = paginator.page(page)
        return render(request, "ProyectoFinalApp/pages.html", {"articulos": articulos, "paginator": paginator, "tab": tab})
 

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
               return redirect("login")
        else:
            return redirect("login")

    form = AuthenticationForm()

    return render(request, 'ProyectoFinalApp/login.html', {'form': form})

def register_request(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            messages.add_message(request, messages.SUCCESS, 'El usuario ha sido creado correctamente')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
               return redirect("login")
        return render(request,"ProyectoFinalApp/registro.html",{"form":form})

    form = UserRegisterForm()

    return render(request, 'ProyectoFinalApp/registro.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect("inicio")

@login_required
def editar_perfil(request,tab):
    user = request.user
    tabs = tab
    if tabs == "personal":
        if request.method == "POST":
            
            form = UserEditForm(request.POST) 

            if form.is_valid():
                tabs = tab
                info = form.cleaned_data
                user.email = info["email"]
                user.first_name = info["first_name"]
                user.last_name = info["last_name"]
                user.set_password(info["password1"])

                user.save()
                return redirect('editar_perfil',tabs)
        else:
            form = UserEditForm(initial={"email":user.email, "first_name":user.first_name, "last_name":user.last_name})
            return render(request,"ProyectoFinalApp/editar_perfil.html",{"form":form,"tabs":tabs})
    elif tabs == "avatar":
        if request.method == "POST":
            
            formulario_avatar = AvatarForm(request.POST, request.FILES)

            if formulario_avatar.is_valid():
                tabs = tab
                
                if Avatar.objects.filter(usuario=user).exists():
                     avatar = Avatar.objects.get(usuario=user)
                     avatar.imagen = formulario_avatar.cleaned_data["imagen"]
                     avatar.save()
                     return redirect('editar_perfil',tabs)
                else:
                    user = User.objects.get(username=request.user.username)
                    avatar = Avatar(usuario=user, imagen=formulario_avatar.cleaned_data["imagen"])
                    avatar.save()
        else:
         tabs = tab
         formulario_avatar = AvatarForm()
        return render(request,"ProyectoFinalApp/editar_perfil.html",{"form":formulario_avatar,"tabs":tabs})
    else:
        if request.method == "POST":
            
            form_link = LinkForm(request.POST) 

            if form_link.is_valid():
                tabs = tab
                if Link.objects.filter(usuario=user).exists():
                    links = Link.objects.get(usuario=user)
                    links.link1 = form_link.cleaned_data["link1"]
                    links.link2 = form_link.cleaned_data["link2"]
                    links.save()
                    return redirect('editar_perfil',tabs)
                else:
                    user = User.objects.get(username=request.user.username)
                    info = form_link.cleaned_data
                    links = Link(usuario=user, link1=info["link1"], link2=info["link2"])
                    links.save() 
                    return redirect('editar_perfil',tabs)      
        else:  
            if Link.objects.filter(usuario=user).exists():
             links = Link.objects.get(usuario=user)
             form_link = LinkForm(initial={"link1":links.link1, "link2":links.link2})
             return render(request,"ProyectoFinalApp/editar_perfil.html",{"form_link":form_link,"tabs":tabs})
            else: 
             form_link = LinkForm()
             return render(request,"ProyectoFinalApp/editar_perfil.html",{"form_link":form_link,"tabs":tabs})

@login_required
def eliminar_usuario(request, user_id):

    user = User.objects.get(id=user_id)
    user.delete()

    return redirect("inicio")

def detalle_articulo(request,articuloID):
    try:
        articulos = articulo.objects.get(id=articuloID)
        return render(request, 'ProyectoFinalApp/detalle_articulo.html', {'articulos': articulos, 'url':url})
    except:
        url = "/media/imagenes/3.jpg"
        return render(request, 'ProyectoFinalApp/detalle_articulo.html', {'articulos': articulos, 'url':url})

@staff_member_required
def eliminar_articulo(request, articulo_id):

    articulos = articulo.objects.get(id=articulo_id)
    articulos.delete()
    tabs="articulo"
    return redirect('panel',tabs)
     
@staff_member_required
def crear_articulo(request):

    if request.method == "POST":
        tabs="articulo"
        formulario = FormArticulo(request.POST, request.FILES)

        if formulario.is_valid():

            info_art = formulario.cleaned_data
        
            articulos = articulo(titulo=info_art["titulo"], subTitulo=info_art["subTitulo"], contenido=info_art["contenido"]
            , autor=info_art["autor"], imagen=formulario.cleaned_data["imagen"])

            articulos.save() 
            messages.add_message(request, messages.SUCCESS, 'El Blog ha sido creado correctamente')
            return redirect('panel',tabs)
        else:
            messages.add_message(request, messages.ERROR, 'El Blog no ha sido creado correctamente')
            return render(request,"ProyectoFinalApp/formulario_articulo.html",{"form":formulario,"accion":"Crear Articulo"})
    

    else:

        formularioVacio = FormArticulo()

        return render(request,"ProyectoFinalApp/formulario_articulo.html",{"form":formularioVacio,"accion":"Crear Articulo"})

@staff_member_required
def editar_articulo(request, articulo_id):
    
    articulos = articulo.objects.get(id=articulo_id)
    tabs="articulo"
    if request.method == "POST":

        formulario = FormArticulo(request.POST)
 
        if formulario.is_valid():

            info_art = formulario.cleaned_data
        
            articulos.titulo = info_art["titulo"]
            articulos.subTitulo = info_art["subTitulo"]
            articulos.contenido = info_art["contenido"]
            articulos.autor = info_art["autor"]
            articulos.save()
            messages.add_message(request, messages.SUCCESS, 'El Blog ha sido editado correctamente')
            return redirect('panel',tabs)
        else:
            messages.add_message(request, messages.ERROR, 'El Blog no ha sido editado correctamente')
    else:        
     formulario = FormArticulo(initial={"titulo":articulos.titulo,"subTitulo":articulos.subTitulo,"contenido":articulos.contenido,"autor":articulos.autor
     ,"fecha_creacion":articulos.fecha_creacion})

    return render(request,"ProyectoFinalApp/formulario_articulo.html",{"form":formulario,"accion":"Editar Articulo"})

@staff_member_required
def panel(request,tab):
        if tab == "articulo":
            if request.method == "POST":
                buscar = request.POST["buscar"]
                tabs=tab
                buscador = articulo.objects.filter( Q(titulo__icontains=buscar) | Q(autor__icontains=buscar) ).values()
                prueba = "Hay articulos"
                return render(request,"ProyectoFinalApp/panel.html",{"buscador":buscador,"tab":tab,"prueba":prueba})
            else:
                articulos = articulo.objects.all()
                if len(articulos) > 0:
                    articulos = articulo.objects.all()
                    page = request.GET.get('page', 1)
                    paginator = Paginator(articulos, 5)
                    articulos = paginator.page(page)
                    prueba = "Hay articulos"
                    return render(request, 'ProyectoFinalApp/panel.html', {'articulos': articulos, 'paginator': paginator, 'tab': tab, 'prueba': prueba})
                else:
                    prueba = None
                    return render(request, 'ProyectoFinalApp/panel.html', {'prueba': prueba, 'tab': tab})
        else:
            if request.method == "POST":
                if 'enviar' in request.POST:  
                 form = UserEditForm(request.POST)
                 if form.is_valid():
                    info = form.cleaned_data
                    usuario_id = request.POST["id"]
                    user = User.objects.get(id=usuario_id)
                    user.first_name = info["first_name"]
                    user.last_name = info["last_name"]
                    user.email = info["email"]
                    user.set_password(info["password1"])
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'El Usuario ha sido editado correctamente')
                    return redirect('panel',tabs)
                 else:
                    messages.add_message(request, messages.SUCCESS, 'El Usuario no ha sido editado correctamente')
                else:
                    buscar = request.POST["buscar"]
                    form = UserEditForm()
                    buscador = User.objects.filter( Q(username__icontains=buscar) | Q(email__icontains=buscar) ).values()
                    prueba = "Hay articulos"
                    return render(request,"ProyectoFinalApp/panel.html",{"buscador":buscador,"tab":tab,"prueba":prueba,"form":form})
            else:
                usuarios = User.objects.filter().values()
                form = UserEditForm()
                if len(usuarios) > 0:
                    usuarios = User.objects.all()
                    page = request.GET.get('page', 1)
                    paginator = Paginator(usuarios, 5)
                    usuarios = paginator.page(page)
                    prueba = "Hay articulos"
                    return render(request, 'ProyectoFinalApp/panel.html', {'usuarios': usuarios, 'paginator': paginator, 'tab': tab, 'prueba': prueba,'form':form})
                else:
                    prueba = None
                    return render(request, 'ProyectoFinalApp/panel.html', {'prueba': prueba, 'tab': tab,'form':form})
 

@login_required
def mensajes(request,mensaje_id):
    if request.method == 'POST':
        form = FormMensaje(request.POST)
        if form.is_valid():
            info_form = form.cleaned_data
            user_autor = User.objects.get(username=request.user)
            contenido = Mensaje.objects.create(usuario_receptor = info_form['usuario_receptor'] ,autor = user_autor,mensaje=info_form['mensaje'])
            contenido.save()
            return redirect('messages',1)
        else:
            form = FormMensaje()
            return render(request, 'ProyectoFinalApp/messages.html', {'form': form})
    else:
        form = FormMensaje()
        buscar = request.GET.get('buscar')
        page = request.GET.get('page', 1)
        if buscar is not None and buscar is not "":
                buscador = Mensaje.objects.filter(usuario_receptor = request.user).filter(Q(autor__username__icontains=buscar)  | Q(mensaje__icontains=buscar))
                paginator = Paginator(buscador, 5)
                buscador = paginator.page(page)
                if mensaje_id == "1":
                    mensajes = Mensaje.objects.filter(usuario_receptor = request.user)[:1].get()
                    return render(request, 'ProyectoFinalApp/messages.html', {'form': form,'buscador':buscador,'paginator':paginator,'mensaje_id':mensaje_id,'buscar':buscar,'mensajes':mensajes})
                else:
                    mensajes = Mensaje.objects.get(usuario_receptor = request.user,id=mensaje_id)
                    return render(request, 'ProyectoFinalApp/messages.html', {'form': form,'buscador':buscador,'paginator':paginator,'mensaje_id':mensaje_id,'buscar':buscar,'mensajes':mensajes})
        else:
            contenido = Mensaje.objects.filter(usuario_receptor = request.user)
            paginator = Paginator(contenido, 5)
            contenido = paginator.page(page)
            if mensaje_id == "1":
                mensajes = Mensaje.objects.filter(usuario_receptor = request.user)[:1].get()
                return render(request, 'ProyectoFinalApp/messages.html', {'form': form,'contenido':contenido,'paginator':paginator,'mensaje_id':mensaje_id,'mensajes':mensajes})
            else:
                mensajes = Mensaje.objects.get(usuario_receptor = request.user,id=mensaje_id)
                return render(request, 'ProyectoFinalApp/messages.html', {'form': form,'contenido':contenido,'paginator':paginator,'mensaje_id':mensaje_id,'mensajes':mensajes})
            
    


@login_required
def eliminar_mensaje(request, mensaje_id):
    mensaje = Mensaje.objects.get(id=mensaje_id)
    mensaje.delete()
    messages.add_message(request, messages.SUCCESS, 'Elimino el mensaje correctamente')
    return redirect("messages",1)


@staff_member_required
def eliminar_usuario_panel(request, usuario_id):
    usuario = User.objects.get(username=usuario_id)
    usuario.delete()
    messages.add_message(request, messages.SUCCESS, 'Elimino al usuario correctamente')
    tab = "usuario"
    return redirect("panel", tab)

@staff_member_required
def dar_permiso(request, usuario_id):
    usuario = User.objects.get(username=usuario_id)
    usuario.is_staff = True
    usuario.save()
    messages.add_message(request, messages.SUCCESS, 'Le otorgo los permisos de admin al usuario')
    tab = "usuario"
    return redirect("panel",tab)


@staff_member_required
def sacar_permiso(request, usuario_id):
    usuario = User.objects.get(username=usuario_id)
    usuario.is_staff = False
    usuario.save()
    messages.add_message(request, messages.SUCCESS, 'Le retiro los permisos de admin al usuario')
    tab = "usuario"
    return redirect("panel",tab)


def test(request,mensaje_id):
    if request.method == 'POST':
        form = FormMensaje(request.POST)
        if form.is_valid():
            info_form = form.cleaned_data
            user_autor = User.objects.get(username=request.user)
            contenido = Mensaje.objects.create(usuario_receptor = info_form['usuario_receptor'] ,autor = user_autor,mensaje=info_form['mensaje'])
            contenido.save()
            return redirect('test',1)
        else:
            form = FormMensaje()
            return render(request, 'ProyectoFinalApp/test.html', {'form': form})
    else:
        form = FormMensaje()
        buscar = request.GET.get('buscar')
        page = request.GET.get('page', 1)
        if buscar is not None and buscar is not "":
                buscador = Mensaje.objects.filter(usuario_receptor = request.user).filter(Q(autor__username__icontains=buscar)  | Q(mensaje__icontains=buscar))
                paginator = Paginator(buscador, 5)
                buscador = paginator.page(page)
                if mensaje_id == "1":
                    mensajes = Mensaje.objects.filter(usuario_receptor = request.user)[:1].get()
                    return render(request, 'ProyectoFinalApp/test.html', {'form': form,'buscador':buscador,'paginator':paginator,'mensaje_id':mensaje_id,'buscar':buscar,'mensajes':mensajes})
                else:
                    mensajes = Mensaje.objects.get(usuario_receptor = request.user,id=mensaje_id)
                    return render(request, 'ProyectoFinalApp/test.html', {'form': form,'buscador':buscador,'paginator':paginator,'mensaje_id':mensaje_id,'buscar':buscar,'mensajes':mensajes})
        else:
            contenido = Mensaje.objects.filter(usuario_receptor = request.user)
            paginator = Paginator(contenido, 5)
            contenido = paginator.page(page)
            if mensaje_id == "1":
                mensajes = Mensaje.objects.filter(usuario_receptor = request.user)[:1].get()
                return render(request, 'ProyectoFinalApp/test.html', {'form': form,'contenido':contenido,'paginator':paginator,'mensaje_id':mensaje_id,'mensajes':mensajes})
            else:
                mensajes = Mensaje.objects.get(usuario_receptor = request.user,id=mensaje_id)
                return render(request, 'ProyectoFinalApp/test.html', {'form': form,'contenido':contenido,'paginator':paginator,'mensaje_id':mensaje_id,'mensajes':mensajes})
    
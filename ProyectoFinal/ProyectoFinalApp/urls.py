
from django.urls import path

from .views import *

urlpatterns = [
    # URLS de ProyectoCoderApp
    path('', inicio, name="inicio"),
    path('nosotros/', nosotros, name="nosotros"),
    path('pages/', pages, name="pages"),
    path('login/', login_request, name="login"),
    path('register/', register_request, name="register"),
    path('logout/', logout_request, name="logout"),
    path('eliminar_usuario/<user_id>', eliminar_usuario, name="eliminar_usuario"),
    path('detalle_articulo/<articuloID>', detalle_articulo, name="detalle_articulo"),
    path('eliminar_articulo/<articulo_id>', eliminar_articulo, name="eliminar_articulo"),
    path('formulario_articulo/', crear_articulo, name="crear_articulo"),
    path('editar_articulo/<articulo_id>', editar_articulo, name="editar_articulo"),
    path('editar_perfil/<str:tab>', editar_perfil, name="editar_perfil"),
    path('panel/<str:tab>', panel, name="panel"),
    path('messages/<mensaje_id>', mensajes, name="messages"),
    path('eliminar_mensaje/<mensaje_id>', eliminar_mensaje, name="eliminar_mensaje"),
    path('eliminar_usuario_panel/<usuario_id>', eliminar_usuario_panel, name="eliminar_usuario_panel"),
    path('dar_permiso/<usuario_id>', dar_permiso, name="dar_permiso"),
    path('sacar_permiso/<usuario_id>', sacar_permiso, name="sacar_permiso"),
    path('test/<mensaje_id>', test, name="test"),
    
    

    
]
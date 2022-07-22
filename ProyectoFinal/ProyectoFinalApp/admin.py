from django.contrib import admin

from.models import *
# Register your models here.


class AritculoAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'subTitulo', 'autor', 'fecha_creacion')
    search_fields = ('titulo', 'subTitulo', 'autor')



class AvatarAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'imagen')
    search_fields = ('usuario', 'imagen')\
        

class MensajeAdmin(admin.ModelAdmin):

    list_display = ('usuario_receptor', 'autor', 'mensaje', 'fecha_creacion')
    search_fields = ('usuario_receptor', 'autor', 'mensaje')


class LinkAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'link1', 'link2')
    search_fields = ('usuario', 'link1', 'link2')

admin.site.register(articulo, AritculoAdmin)

admin.site.register(Avatar, AvatarAdmin)

admin.site.register(Mensaje, MensajeAdmin)

admin.site.register(Link, LinkAdmin)





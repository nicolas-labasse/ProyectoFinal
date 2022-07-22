from django.test import TestCase

from ProyectoFinalApp.models import *

# Create your tests here.


class BlogTest(TestCase):
    def setUp(self):
        articulo.objects.create(titulo = "Nuevo", subTitulo = "Nuevosub", contenido = "Contenido", autor = "Nicolas", imagen = "Imagen", fecha_creacion = "23/12/2019")
    

    def test_articulo_titulo(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertEqual(articulo_nuevo.titulo, "Nuevo")

    def test_articulo_subTitulo(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertEqual(articulo_nuevo.subTitulo, "Nuevosub")

    def test_articulo_contenido(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertEqual(articulo_nuevo.contenido, "Contenido")

    def test_articulo_autor(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertEqual(articulo_nuevo.autor, "Nicolas")

    def test_articulo_imagen(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertEqual(articulo_nuevo.imagen, "Imagen")


    def test_articulo_creado(self):
        articulo_nuevo = articulo.objects.get(titulo = "Nuevo")
        self.assertTrue(articulo_nuevo, None)

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(username = "Nicolas", password = "123456")
    

    def test_user_username(self):
        user_nicolas = User.objects.get(username = "Nicolas")
        self.assertEqual(user_nicolas.username, "Nicolas")
    
    def test_user_pass(self):
        user_nicolas = User.objects.get(password = "123456")
        self.assertEqual(user_nicolas.password, "123456")


    def test_user_creado(self):
        user_nico = User.objects.get(username = "Nicolas")
        self.assertTrue(user_nico, None)
from user.models import User
from django.test import TestCase, Client
from django.urls import reverse
from GestionClientes.models import Cliente, Sucursale


class ClienteViewTest(TestCase):

    def setUp(self):
        # Se crea un cliente y un usuario para ser usados en las pruebas

        self.cliente = Cliente.objects.create(identificacion="1234567890", nombre="Juan", direccion="Calle 123",
                                              ciudad="Bogotá", email="juan@example.com", telefono="1234567", activo=True)
        self.usuario = User.objects.create_user(
            username='usuario1', password='contraseña1')

    def test_lista_clientes_view(self):
        # Se inicia sesión con el usuario creado
        self.client.login(username='usuario1', password='contraseña1')
        # Se realiza una solicitud GET a la vista de lista de clientes
        response = self.client.get(reverse('clientes'))
        # Se verifica que la respuesta sea satisfactoria
        self.assertEqual(response.status_code, 200)
        # Se verifica que el nombre del cliente creado se encuentre en la respuesta
        self.assertContains(response, self.cliente.nombre)

    def test_detalle_cliente_view(self):
        # Se realiza una solicitud GET a la vista de detalle del cliente creado
        response = self.client.get(
            reverse('detalle_cliente', args=[self.cliente.id]))
        # Se verifica que la respuesta sea satisfactoria
        self.assertEqual(response.status_code, 200)
        # Se verifica que los detalles del cliente se encuentren en la respuesta
        self.assertContains(response, self.cliente.nombre)
        self.assertContains(response, self.cliente.direccion)
        self.assertContains(response, self.cliente.ciudad)
        self.assertContains(response, self.cliente.email)
        self.assertContains(response, self.cliente.telefono)

    def test_create_cliente_view(self):
        # Se crea un diccionario con los datos para crear un nuevo cliente
        data = {
            'identificacion': '1234567891',
            'nombre': 'Pedro',
            'direccion': 'Calle 456',
            'ciudad': 'Medellín',
            'email': 'pedro@example.com',
            'telefono': '7654321',
            'activo': True
        }
        # Se realiza una solicitud POST a la vista de creación de cliente con los datos creados
        response = self.client.post(reverse('create_cliente'), data=data)
        # Se verifica que la respuesta sea de redireccionamiento
        self.assertEqual(response.status_code, 302)
        # Se busca el cliente creado en la base de datos y se verifican sus datos
        cliente_creado = Cliente.objects.get(
            identificacion=data['identificacion'])
        self.assertEqual(cliente_creado.nombre, data['nombre'])
        self.assertEqual(cliente_creado.direccion, data['direccion'])
        self.assertEqual(cliente_creado.ciudad, data['ciudad'])
        self.assertEqual(cliente_creado.email, data['email'])
        self.assertEqual(cliente_creado.telefono, data['telefono'])
        self.assertEqual(cliente_creado.activo, data['activo'])

    def test_editar_cliente_view(self):
        # Comprobamos que la vista para editar un cliente funciona correctamente
        url = reverse('editar_cliente', args=[self.cliente.id])
        url = reverse('editar_cliente', args=[self.cliente.id])
        data = {
            'identificacion': '1234567890',
            'nombre': 'Juan Pablo',
            'direccion': 'Calle 123',
            'ciudad': 'Bogotá',
            'email': 'juanpablo@example.com',
            'telefono': '1234567',
            'activo': True
        }
        response = self.client.post(url, data=data)
        # Se verifica que la respuesta sea de redireccionamiento
        self.assertEqual(response.status_code, 302)
        # Comprobamos que el cliente editado existe en la base de datos
        cliente_editado = Cliente.objects.get(id=self.cliente.id)
        self.assertEqual(cliente_editado.nombre, data['nombre'])
        self.assertEqual(cliente_editado.direccion, data['direccion'])
        self.assertEqual(cliente_editado.ciudad, data['ciudad'])
        self.assertEqual(cliente_editado.email, data['email'])
        self.assertEqual(cliente_editado.telefono, data['telefono'])
        self.assertEqual(cliente_editado.activo, data['activo'])

    def test_eliminar_cliente_view(self):
        # Se genera la URL para eliminar el cliente utilizando la función reverse y pasando el ID del cliente como argumento
        url = reverse('eliminar_cliente', args=[self.cliente.id])
        # Se realiza una petición POST a la URL de eliminar cliente
        response = self.client.post(url)
        # Se verifica que la respuesta tenga un código de estado 302, que indica una redirección
        self.assertEqual(response.status_code, 302)
        # Se obtiene el objeto del cliente eliminado de la base de datos utilizando su ID y se verifica que su campo 'activo' sea False
        cliente_eliminado = Cliente.objects.get(id=self.cliente.id)
        self.assertFalse(cliente_eliminado.activo)


class SucursalViewsTest(TestCase):
    def setUp(self):
        # Se crea un cliente y un usuario para ser usados en las pruebas

        self.cliente = Cliente.objects.create(identificacion="1234567890", nombre="Juan", direccion="Calle 123",
                                              ciudad="Bogotá", email="juan@example.com", telefono="1234567", activo=True)
        
        
        self.usuario = User.objects.create_user(
            username='usuario1', password='contraseña1')
        # El usuario inicia sesión
        self.client.login(username='usuario1', password='contraseña1')
        # Se crea una sucursal para el cliente
        self.sucursal = Sucursale.objects.create(nombre="Sucursal de prueba",
                                                 direccion="Dirección de prueba",
                                                 telefono="1234567890",
                                                 ciudad="Ciudad de prueba",
                                                 cliente=self.cliente)
    # Prueba para la vista que lista todas las sucursales del usuario cliente
    def test_sucursal_view(self):
        url = reverse('sucursales')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sucursales/index.html')

    # Prueba para la vista que muestra el detalle de una sucursal
    def test_detalle_sucursal_view(self):
        url = reverse('detalle_sucursal', args=[self.sucursal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sucursales/detail.html')
        # Se verifica que la sucursal sea la misma que la creada en setUp
        self.assertEqual(response.context['sucursal'], self.sucursal)

    # Prueba para la vista que permite editar una sucursal existente
    def test_editar_sucursal_view(self):
        url = reverse('editar_sucursal', args=[self.sucursal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sucursales/edit.html')
         # Se crea un diccionario con los datos actualizados de la sucursal
        data = {
            'nombre': 'Sucursal de prueba 3',
            'direccion': 'Dirección de prueba 3',
            'telefono': '1111111111',
            'ciudad': 'Ciudad de prueba 3'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.sucursal.refresh_from_db()
        # Se verifica que los datos de la sucursal hayan sido actualizados correctamente
        self.assertEqual(self.sucursal.nombre, 'Sucursal de prueba 3')
        self.assertEqual(self.sucursal.direccion, 'Dirección de prueba 3')
        self.assertEqual(self.sucursal.telefono, '1111111111')
        self.assertEqual(self.sucursal.ciudad, 'Ciudad de prueba 3')

    def test_eliminar_sucursal(self):
        cliente = self.cliente
        sucursal = self.sucursal
        url = reverse('eliminar_sucursal', args=[sucursal.id])
        response = self.client.get(url)
        # Verifica que la respuesta sea una redirección a la lista de sucursales
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('sucursales'))
        # Verifica que la sucursal haya sido eliminada correctamente
        sucursal_eliminada = Sucursale.objects.filter(
            pk=sucursal.id, activo=False).exists()
        self.assertTrue(sucursal_eliminada)

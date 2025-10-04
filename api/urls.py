from django.urls import path
from api.views.cliente_view import ClienteView
from api.views.categoria_view import CategoriaView
from api.views.producto_view import ProductoView
from api.views.notaventa_view import NotaVentaView
from api.views.detalleventa_view import DetalleVentaView


urlpatterns = [
    # CRUD de Cliente
    path("clientes/", ClienteView.as_view(), name="cliente-list-create"),
    path("clientes/<int:pk>/", ClienteView.as_view(), name="cliente-detail"),
    path('categorias/', CategoriaView.as_view(), name='categoria-list'),
    path('categorias/<int:pk>/', CategoriaView.as_view(), name='categoria-detail'), #<int:categoria_id> se podria llamar asi tambien
    path("productos/", ProductoView.as_view(), name="producto-list-create"),
    path("productos/<int:pk>/", ProductoView.as_view(), name="producto-detail"),
    path("notas/", NotaVentaView.as_view(), name="notaventa-list-create"),
    path("notas/<int:pk>/", NotaVentaView.as_view(), name="notaventa-detail"),
    path("detalleventas/", DetalleVentaView.as_view(), name="detalleventa-list-create"),             # listar todos o crear
    path("detalleventas/<int:pk>/", DetalleVentaView.as_view(), name="detalleventa-detail"),         # actualizar / eliminar
    path("notaventas/<int:notaventa_id>/detalleventas/", DetalleVentaView.as_view(), name="detalleventa-by-nota"),

]

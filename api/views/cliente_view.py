from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers.cliente_serializer import ClienteSerializer
from core.use_cases.registrar_cliente import RegistrarCliente
from core.use_cases.actualizar_cliente import ActualizarCliente
from core.use_cases.eliminar_cliente import EliminarCliente
from core.use_cases.listar_clientes import ListarClientes
from infrastructure.repositories.cliente_django_repository import ClienteDjangoRepository


class ClienteView(APIView):
    """
    APIView para manejar operaciones CRUD de Cliente.
    Cada método delega en un caso de uso correspondiente.
    """

    def get(self, request, pk=None):
        if pk:
            # obtener cliente por id
            cliente = ClienteDjangoRepository().get_by_id(pk)
            if not cliente:
                return Response({"detail": "Cliente no encontrado"}, status=404)
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        else:
            # listar todos los clientes
            clientes = ClienteDjangoRepository().list_all()
            serializer = ClienteSerializer(clientes, many=True)
            return Response(serializer.data)

    def post(self, request):
        """Registrar un cliente"""
        serializer = ClienteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repository = ClienteDjangoRepository()
        use_case = RegistrarCliente(repository)
        cliente = use_case.execute(serializer.validated_data)

        output_serializer = ClienteSerializer(cliente)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        """Actualizar un cliente existente"""
        serializer = ClienteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repository = ClienteDjangoRepository()
        use_case = ActualizarCliente(repository)
        cliente = use_case.execute(pk, serializer.validated_data)

        output_serializer = ClienteSerializer(cliente)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """Eliminar un cliente"""
        repository = ClienteDjangoRepository()
        use_case = EliminarCliente(repository)
        use_case.execute(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

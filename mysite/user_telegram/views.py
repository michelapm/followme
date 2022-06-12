from rest_framework import viewsets
from .serializer import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UsersTelegramViewSet(viewsets.ModelViewSet):
    queryset = UsersTelegram.objects.all()
    serializer_class = UsersTelegramSerializer


class UsersTelegramRegistradosViewSet(viewsets.ModelViewSet):
    queryset = UsersTelegram.objects.filter(estado=True)
    serializer_class = UsersTelegramSerializer


class MetodosPagosViewSet(viewsets.ModelViewSet):
    queryset = MetodosPagos.objects.filter(
        estado=True
    )
    serializer_class = MetodosPagosSerializer


class ReaccionViewSet(viewsets.ModelViewSet):
    queryset = Reaccion.objects.filter(
        estado=True
    )
    serializer_class = ReaccionSerializer


class RedesViewSet(viewsets.ModelViewSet):
    queryset = Redes.objects.filter(
        estado=True
    )
    serializer_class = RedeSerializer


class GaleriaViewSet(viewsets.ModelViewSet):
    queryset = Galeria.objects.filter(
        estado=True
    )
    serializer_class = GaleriaSerializer


class UserRedesViewSet(viewsets.ModelViewSet):
    queryset = UserRedes.objects.all()
    serializer_class = UserRedeSerializer


class UsersMetodosPagosViewSet(viewsets.ModelViewSet):
    queryset = UsersMetodosPagos.objects.all()
    serializer_class = UsersMetodosPagoSerializer


class UsersReaccionViewSet(viewsets.ModelViewSet):
    queryset = UsersReaccion.objects.all()
    serializer_class = UsersReaccionSerializer


class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer


class PlanesViewSet(viewsets.ModelViewSet):
    queryset = Planes.objects.filter(
        estado=True
    )
    serializer_class = PlanesSerializer


@api_view(['GET'])
def referidos_detail(request, pk):
    referidos = UsersTelegram.objects.filter(referido=pk)
    cantidad = len(list(referidos))

    if request.method == 'GET':
        return Response({'cant': cantidad})


@api_view(['GET'])
def reacciones_detail(request, client_id, messageid):
    userreaccion = UsersReaccion.objects.filter(message=messageid, actor=client_id)

    if request.method == 'GET':
        serializer = UsersReaccionSerializer(userreaccion, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def cant_reacciones_detail(request, reaccionid, messageid):
    userreaccion = UsersReaccion.objects.filter(id_reaccion=reaccionid, message=messageid)
    cantidad = len(list(userreaccion))
    if request.method == 'GET':
        return Response({'cant': cantidad})


@api_view(['DELETE'])
def eliminar_user_redes(request, user):
    user_redes = list(UserRedes.objects.filter(user=user))
    if request.method == 'DELETE':
        for user_red in user_redes:
            user_red.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ultima_publicacion_user(request, user):
    try:
        ultima_pub_user = Publicacion.objects.filter(client_id=user).order_by('-fecha_publicacion')[0]
    except:
        return Response({'ultima_pub_user': 'No hay publicaciones'}, status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PublicacionSerializer(ultima_pub_user)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def galeria_user(request, user):
    try:
        galeria_users = Galeria.objects.filter(client_id=user)
    except:
        return Response({'error': 'Erroe en la consulta'}, status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = GaleriaSerializer(galeria_users, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        for galeria in list(galeria_users):
            galeria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


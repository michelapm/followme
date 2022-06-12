from rest_framework import serializers
from .models import *


class UsersTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTelegram
        fields = '__all__'


class MetodosPagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodosPagos
        fields = '__all__'


class ReaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaccion
        fields = '__all__'


class RedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redes
        fields = '__all__'


class UsersMetodosPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersMetodosPagos
        fields = '__all__'


class UserRedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRedes
        fields = '__all__'


class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeria
        fields = '__all__'


class UsersReaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersReaccion
        fields = '__all__'


class PlanesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planes
        fields = '__all__'


class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

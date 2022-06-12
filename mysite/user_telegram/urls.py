from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
from django.urls import path, re_path
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Documentación de API",
        default_version='v1',
        description="Documentacion publica API de mi Restaurante",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
route = routers.SimpleRouter()
route.register('userstelegram', UsersTelegramViewSet)
route.register('userstelegramregistrado', UsersTelegramRegistradosViewSet)
route.register('metodospagos', MetodosPagosViewSet)
route.register('reaccion', ReaccionViewSet)
route.register('redes', RedesViewSet)
route.register('galeria', GaleriaViewSet)
route.register('usersreaccion', UsersReaccionViewSet)
route.register('userredes', UserRedesViewSet)
route.register('userpago', UsersMetodosPagosViewSet)
route.register('publicacion', PublicacionViewSet)
route.register('planes', PlanesViewSet)

urlpatterns = [
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('referidos_detail/<int:pk>/', referidos_detail),
                  path('reaccionesuser/<int:client_id>/<int:messageid>/', reacciones_detail),
                  path('reaccioncant/<int:reaccionid>/<int:messageid>/', cant_reacciones_detail),
                  path('uredesdelete/<int:user>/', eliminar_user_redes),
                  path('ultimapublicacionuser/<int:user>/', ultima_publicacion_user),
                  path('galeriauser/<int:user>/', galeria_user),
              ] + route.urls

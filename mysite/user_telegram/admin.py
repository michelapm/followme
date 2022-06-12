from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UsersTelegramResource(resources.ModelResource):
    class Meta:
        model: UsersTelegram
        exclude = ('nombre',)


class MetodosPagosResource(resources.ModelResource):
    class Meta:
        model: MetodosPagos


class PublicacionResource(resources.ModelResource):
    class Meta:
        model: Publicacion


class ReaccionResource(resources.ModelResource):
    class Meta:
        model: Reaccion


class RedesResource(resources.ModelResource):
    class Meta:
        model: Redes


class GaleriaResource(resources.ModelResource):
    class Meta:
        model: Galeria


class UsersReaccionResource(resources.ModelResource):
    class Meta:
        model: UsersReaccion


class UsersMetodosPagosResource(resources.ModelResource):
    class Meta:
        model: UsersMetodosPagos


class UserRedesResource(resources.ModelResource):
    class Meta:
        model: UserRedes


class PlanesResource(resources.ModelResource):
    class Meta:
        model: Planes


class UsersTelegramAdmin(ImportExportModelAdmin):
    resource_class = UsersTelegramResource
    list_display = ('nombre', 'client_id', 'referido', 'descripcion')
    search_fields = ['nombre', 'client_id']


class PublicacionAdmin(ImportExportModelAdmin):
    resource_class = PublicacionResource


class PlanesAdmin(ImportExportModelAdmin):
    resource_class = PlanesResource


class MetodosPagosAdmin(ImportExportModelAdmin):
    resource_class = MetodosPagosResource
    list_display = ('nombre',)
    search_fields = ['nombre']


class ReaccionAdmin(ImportExportModelAdmin):
    resource_class = ReaccionResource
    list_display = ('nombre',)
    search_fields = ['nombre']


class RedesAdmin(ImportExportModelAdmin):
    resource_class = RedesResource
    list_display = ('nombre',)
    search_fields = ['nombre']


class GaleriaAdmin(ImportExportModelAdmin):
    resource_class = GaleriaResource


class UsersReaccionAdmin(ImportExportModelAdmin):
    resource_class = UsersReaccionResource


class UsersMetodosPagosAdmin(ImportExportModelAdmin):
    resource_class = UsersMetodosPagosResource


class UserRedesAdmin(ImportExportModelAdmin):
    resource_class = UserRedesResource


admin.site.register(UsersTelegram, UsersTelegramAdmin)
admin.site.register(MetodosPagos, MetodosPagosAdmin)
admin.site.register(Reaccion, RedesAdmin)
admin.site.register(Redes, RedesAdmin)
admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(UsersReaccion, UsersReaccionAdmin)
admin.site.register(UsersMetodosPagos, UsersMetodosPagosAdmin)
admin.site.register(UserRedes, UserRedesAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(Planes, PlanesAdmin)

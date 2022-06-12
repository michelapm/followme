from django.db import models


class ModeloBase(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    fecha_modificacion = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True


class Planes(ModeloBase):
    nombre = models.CharField('Nombre del Plan', max_length=50)
    descripcion = models.TextField('Descripcion del plan')
    precio = models.FloatField('Precio del plan')
    horas_republicacion = models.IntegerField('Cantidad de horas para poder publicar de nuevo')
    automatic = models.BooleanField('Estado de republicacion automatico', default=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return str(self.nombre)


class UsersTelegram(models.Model):
    estado = models.BooleanField('Estado del Usuario', default=False)
    fecha_creacion = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    fecha_modificacion = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)
    client_id = models.IntegerField('ID de telegram del usuario', primary_key=True)
    referido = models.IntegerField('Referido', blank=True, null=True)
    nombre = models.CharField('Nombre del Usuario', max_length=50, blank=True, null=True)
    descripcion = models.TextField('Descripcion del usuario', blank=True, null=True)
    foto = models.CharField('Ruta de la foto', max_length=200, blank=True, null=True)
    ultimomsg = models.CharField('ultimo sms', max_length=50, blank=True, null=True)
    saldo_cup = models.FloatField('Saldo de referidos en cup', default=0)
    saldo_usdt = models.FloatField('Saldo de referidos en usd', default=0)
    saldo_mlc = models.FloatField('Saldo de referidos en mlc', default=0)
    saldo_movil = models.FloatField('Saldo de referidos en movil', default=0)
    plan = models.ForeignKey(Planes, on_delete=models.PROTECT, default=1)

    class Meta:
        ordering = ['fecha_creacion']
        verbose_name = 'User Telegram'
        verbose_name_plural = 'Users Telegram'

    def __str__(self):
        return f'{self.client_id} --> {self.nombre}'


class MetodosPagos(ModeloBase):
    nombre = models.CharField('Metodo de pago', max_length=100)
    direccion = models.CharField('Direccion de pago', max_length=200, blank=True, null=True)
    siglas = models.CharField('Siglas', max_length=20)
    mensaje_guia = models.TextField('Mensaje que ve el usuario')
    valor_cambio = models.FloatField('Valor del cambio', default=1)

    class Meta:
        ordering = ['id']
        verbose_name = 'Metodo de Pago'
        verbose_name_plural = 'Metodo de Pagos'

    def __str__(self):
        return self.nombre


class UsersMetodosPagos(models.Model):
    metodo = models.ForeignKey(MetodosPagos, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersTelegram, on_delete=models.CASCADE)
    fecha_pago = models.DateField('Fecha de Pago', auto_now=True)

    class Meta:
        ordering = ['fecha_pago']
        verbose_name = 'User Metodo Pago'
        verbose_name_plural = 'Users Metodos Pagos'

    def __str__(self):
        return f'{self.metodo} -> {self.user} -> {self.fecha_pago}'


class Reaccion(ModeloBase):
    nombre = models.CharField('Nombre de la reaccion', max_length=100)

    class Meta:
        ordering = ['id']
        verbose_name = 'Reaccion'
        verbose_name_plural = 'Reacciones'

    def __str__(self):
        return self.nombre


class Redes(ModeloBase):
    nombre = models.CharField('Nombre de la red social', max_length=100, unique=True)
    url = models.URLField('Direccion de la red socioal')

    class Meta:
        ordering = ['id']
        verbose_name = 'Rede'
        verbose_name_plural = 'Redes'

    def __str__(self):
        return self.nombre


class UserRedes(ModeloBase):
    redes = models.ForeignKey(Redes, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersTelegram, on_delete=models.CASCADE)
    username = models.CharField('ruta de la red social', max_length=100)

    class Meta:
        verbose_name = 'UserRede'
        verbose_name_plural = 'UserRedes'

    def __str__(self):
        return f'{self.user} -> {self.redes} '


class Galeria(ModeloBase):
    fotos_galeria = models.CharField('Ruta de la foto', max_length=100)
    client_id = models.ForeignKey(UsersTelegram, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galerias'

    def __str__(self):
        return str(self.client_id)


class Publicacion(models.Model):
    fecha_publicacion = models.DateTimeField('Fecha de la publicacion', auto_now=True)
    message = models.IntegerField('Publicacion id', primary_key=True)
    client_id = models.ForeignKey(UsersTelegram, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha_publicacion']
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicacionnes'

    def __str__(self):
        return f'{self.fecha_publicacion} -> {self.client_id}'


class UsersReaccion(ModeloBase):
    id_reaccion = models.ForeignKey(Reaccion, on_delete=models.CASCADE)
    actor = models.IntegerField('El que reacciona')
    message = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'UsersReaccion'
        verbose_name_plural = 'UsersReacciones'

    def __str__(self):
        return str(self.actor)

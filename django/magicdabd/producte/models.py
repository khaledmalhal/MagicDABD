# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Carta(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=150)
    rareza = models.CharField(max_length=2)
    tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'carta'


class Ciudad(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)  # The composite primary key (nombre, provincia) found, that is not supported. The first column is selected.
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='provincia')

    class Meta:
        managed = False
        db_table = 'ciudad'
        unique_together = (('nombre', 'provincia'),)


class Copia(models.Model):
    cantidad = models.IntegerField()
    carta = models.OneToOneField(Carta, models.DO_NOTHING, db_column='carta', primary_key=True)  # The composite primary key (carta, propietario) found, that is not supported. The first column is selected.
    propietario = models.ForeignKey('Jugador', models.DO_NOTHING, db_column='propietario')

    class Meta:
        managed = False
        db_table = 'copia'
        unique_together = (('carta', 'propietario'),)


class Deck(models.Model):
    creacion = models.DateField()
    propietario = models.ForeignKey('Jugador', models.DO_NOTHING, db_column='propietario')

    class Meta:
        managed = False
        db_table = 'deck'
        unique_together = (('id', 'propietario'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inventario(models.Model):
    cantidad = models.IntegerField()
    tienda = models.OneToOneField('Tienda', models.DO_NOTHING, db_column='tienda', primary_key=True)  # The composite primary key (tienda, carta) found, that is not supported. The first column is selected.
    carta = models.ForeignKey(Carta, models.DO_NOTHING, db_column='carta')

    class Meta:
        managed = False
        db_table = 'inventario'
        unique_together = (('tienda', 'carta'),)


class Jugador(models.Model):
    nif = models.CharField(primary_key=True, max_length=9)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=40)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='ciudad')
    provincia = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'jugador'


class Participante(models.Model):
    jugador = models.OneToOneField(Jugador, models.DO_NOTHING, db_column='jugador', primary_key=True)  # The composite primary key (jugador, fecha, ciudad, provincia) found, that is not supported. The first column is selected.
    fecha = models.ForeignKey('Torneo', models.DO_NOTHING, db_column='fecha')
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'participante'
        unique_together = (('jugador', 'fecha', 'ciudad', 'provincia'),)


class Partida(models.Model):
    duelista1 = models.OneToOneField(Jugador, models.DO_NOTHING, db_column='duelista1', primary_key=True)  # The composite primary key (duelista1, duelista2, fecha, ciudad, provincia) found, that is not supported. The first column is selected.
    duelista2 = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='duelista2', related_name='partida_duelista2_set')
    ganador = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='ganador', related_name='partida_ganador_set', blank=True, null=True)
    deck1 = models.ForeignKey(Deck, models.DO_NOTHING, db_column='deck1')
    deck2 = models.ForeignKey(Deck, models.DO_NOTHING, db_column='deck2', related_name='partida_deck2_set')
    fecha = models.ForeignKey('Torneo', models.DO_NOTHING, db_column='fecha')
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'partida'
        unique_together = (('duelista1', 'duelista2', 'fecha', 'ciudad', 'provincia'),)


class Provincia(models.Model):
    nombre = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'provincia'


class Repetido(models.Model):
    cantidad = models.IntegerField()
    carta = models.OneToOneField(Carta, models.DO_NOTHING, db_column='carta', primary_key=True)  # The composite primary key (carta, deck, propietario) found, that is not supported. The first column is selected.
    deck = models.ForeignKey(Deck, models.DO_NOTHING, db_column='deck')
    propietario = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'repetido'
        unique_together = (('carta', 'deck', 'propietario'),)


class Tienda(models.Model):
    nombre = models.CharField(primary_key=True, max_length=100)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='ciudad')
    provincia = models.CharField(max_length=40)
    telefono = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'tienda'


class Torneo(models.Model):
    fecha = models.DateField(primary_key=True)  # The composite primary key (fecha, ciudad, provincia) found, that is not supported. The first column is selected.
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='ciudad')
    provincia = models.CharField(max_length=40)
    ganador = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='ganador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'torneo'
        unique_together = (('fecha', 'ciudad', 'provincia'),)


class Transaccion(models.Model):
    carta = models.ForeignKey(Carta, models.DO_NOTHING, db_column='carta')
    cede = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='cede', blank=True, null=True)
    recibe = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='recibe', related_name='transaccion_recibe_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaccion'


class Vendida(models.Model):
    cantidad = models.IntegerField()
    carta = models.OneToOneField(Carta, models.DO_NOTHING, db_column='carta', primary_key=True)  # The composite primary key (carta, factura) found, that is not supported. The first column is selected.
    factura = models.ForeignKey('Venta', models.DO_NOTHING, db_column='factura')
    vendedor = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'vendida'
        unique_together = (('carta', 'factura'),)


class Venta(models.Model):
    idfactura = models.AutoField(primary_key=True)  # The composite primary key (idfactura, vendedor) found, that is not supported. The first column is selected.
    fecha = models.DateField()
    vendedor = models.ForeignKey(Tienda, models.DO_NOTHING, db_column='vendedor')
    cliente = models.ForeignKey(Jugador, models.DO_NOTHING, db_column='cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'venta'
        unique_together = (('idfactura', 'vendedor'),)

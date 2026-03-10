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


class CoreArtist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'core_artist'


class CoreTrack(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(CoreArtist, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_track'
        unique_together = (('title', 'artist'),)


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


class Tblannualwinners(models.Model):
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    artist = models.CharField(db_column='Artist', max_length=255, blank=True, null=True)  # Field name made lowercase.
    album = models.CharField(db_column='Album', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblAnnualWinners'


class Tblshowdetails(models.Model):
    show_id = models.DecimalField(db_column='Show_ID', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    show_date = models.DateField(db_column='Show_Date', blank=True, null=True)  # Field name made lowercase.
    album_of_the_week = models.CharField(db_column='Album_of_the_Week', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year_in_britpop = models.SmallIntegerField(db_column='Year_in_Britpop', blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sotw_stat = models.CharField(db_column='SotW Stat', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'tblShowDetails'


class Tbltracklisting(models.Model):
    track_id = models.IntegerField(db_column='Track_ID', blank=True, null=True)  # Field name made lowercase.
    show_id = models.DecimalField(db_column='Show_ID', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    play_order = models.IntegerField(db_column='Play_Order', blank=True, null=True)  # Field name made lowercase.
    artist = models.CharField(db_column='Artist', max_length=255, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblTrackListing'

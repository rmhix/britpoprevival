from django.db import models


# ============================================================
#  NEW DJANGO-MANAGED MODELS (Artist + Track)
# ============================================================

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="tracks")

    class Meta:
        ordering = ["title"]
        unique_together = ("title", "artist")

    def __str__(self):
        return f"{self.title} — {self.artist.name}"


# ============================================================
#  LEGACY / AUTO-GENERATED TABLES (UNMANAGED)
# ============================================================

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


class AnnualWinner(models.Model):
    year = models.IntegerField(db_column='Year', primary_key=True)
    artist = models.CharField(db_column='Artist', max_length=255, blank=True, null=True)
    album = models.CharField(db_column='Album', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblAnnualWinners'
        verbose_name = "Annual Winner"
        verbose_name_plural = "Annual Winners"

    def __str__(self):
        return f"{self.year} – {self.artist}"


class ShowDetail(models.Model):
    show_id = models.CharField(db_column='Show_ID', max_length=10, primary_key=True)
    show_date = models.DateTimeField(db_column='Show_Date', blank=True, null=True)
    album_of_the_week = models.CharField(db_column='Album_of_the_Week', max_length=255, blank=True, null=True)
    year_in_britpop = models.SmallIntegerField(db_column='Year_in_Britpop', blank=True, null=True)
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)
    sotw_stat = models.CharField(db_column='SotW Stat', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblShowDetails'
        verbose_name = "Show Detail"
        verbose_name_plural = "Show Details"

    def __str__(self):
        return f"Show {self.show_id}"


class TrackListing(models.Model):
    track_id = models.IntegerField(db_column='Track_ID', primary_key=True)

    show = models.ForeignKey(
        ShowDetail,
        on_delete=models.DO_NOTHING,
        db_column='Show_ID',
        related_name='tracks'
    )

    canonical_track = models.ForeignKey(
        'Track',
        on_delete=models.DO_NOTHING,
        db_column='track_fk',
        related_name='tracklist',
        null=True,
        blank=True
    )

    play_order = models.IntegerField(db_column='Play_Order', blank=True, null=True)
    artist = models.CharField(db_column='Artist', max_length=255, blank=True, null=True)
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)
    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)
    notes = models.CharField(db_column='Notes', max_length=5, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'tblTrackListing'
        verbose_name = "Track Listing"
        verbose_name_plural = "Track Listings"

    def __str__(self):
        return f"{self.play_order}. {self.artist} – {self.title}"
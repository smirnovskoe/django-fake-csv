from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Schema(TimeStampedModel):
    class StringCharacter(models.TextChoices):
        SINGLE_QUOTES = "'", _("Single quotes")
        DOUBLE_QUOTES = "\"", _("Double quotes")

    class ColumnSeparator(models.TextChoices):
        COMMA = ',', _("Comma")
        SEMICOLON = ';', _("Semicolon")

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schemas'
    )
    name = models.CharField(max_length=255)

    column_separator = models.CharField(
        max_length=1,
        choices=ColumnSeparator.choices,
        default=ColumnSeparator.COMMA,
    )

    string_character = models.CharField(
        max_length=1,
        choices=StringCharacter.choices,
        default=StringCharacter.SINGLE_QUOTES,
    )

    def __str__(self):
        return self.name


class SchemaColumn(TimeStampedModel):
    class ColumnTypes(models.TextChoices):
        JOB = "job", _("Job")
        COMPANY = 'company', _("Company")
        FULLNAME = 'full_name', _("Full Name")
        PHONE = 'phone', _("Phone")
        ADDRESS = 'address', _("Address")
        EMAIL = 'email', _("Email")
        DOMAIN = 'domain_name', _("Domain name")
        DATE = 'date', _("Date")

    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='columns',
    )

    column_name = models.CharField(max_length=255)

    type = models.CharField(
        max_length=255,
        choices=ColumnTypes.choices,
        default=ColumnTypes.JOB

    )

    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(1), ]

    )

    def __str__(self):
        return f'{self.schema} {self.column_name}'


class Dataset(TimeStampedModel):
    csv_file = models.FileField(
        upload_to='datasets/',
        null=True,
        blank=True,
    )

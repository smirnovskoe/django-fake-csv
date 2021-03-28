from django import forms
from django.forms.models import inlineformset_factory

from . import models


class SchemaColumnModelForm(forms.ModelForm):
    class Meta:
        model = models.SchemaColumn
        exclude = ()


SchemaColumnFormSet = inlineformset_factory(
    models.Schema,
    models.SchemaColumn,
    form=SchemaColumnModelForm,
    extra=1,
    can_delete=True,
)


class SchemaModelForm(forms.ModelForm):
    class Meta:
        model = models.Schema
        exclude = ('creator',)

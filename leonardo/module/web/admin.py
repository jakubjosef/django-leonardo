
from django import forms
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from feincms.admin import item_editor, tree_editor
from feincms.admin.item_editor import FeinCMSInline, ItemEditorForm
from feincms.module.page.modeladmins import PageAdmin as FeinPageAdmin

from .models import *


class PageDimensionAdmin(InlineModelAdmin):

    model = PageDimension


class PageAdmin(FeinPageAdmin):

    fieldsets = [
        (None, {
            'fields': [
                ('title', 'slug'),
                ('active', 'in_navigation'),
            ],
        }),
        (_('Other options'), {
            'classes': ['collapse'],
            'fields': [
                'template_key', 'parent', 'override_url', 'redirect_to', 'theme'],
        }),
        # <-- insertion point, extensions appear here, see insertion_index
        # above
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

admin.site.register(Page, PageAdmin)


class PageDimensionAdmin(ModelAdmin):

    pass

admin.site.register(PageDimension, PageDimensionAdmin)


class WidgetDimensionAdmin(ModelAdmin):

    pass

admin.site.register(WidgetDimension, WidgetDimensionAdmin)


class WidgetThemeForm(forms.ModelForm):

    widget_class = forms.ChoiceField(
        choices=[],
        required=False,
    )

    class Meta:

        model = WidgetTheme

    def __init__(self, *args, **kwargs):
        super(WidgetThemeForm, self).__init__(*args, **kwargs)

        choices = [(t.model_class().__name__ if t.model_class() else None, t)
                   for t in ContentType.objects.filter(app_label__in=['web'])]
        self.fields['widget_class'].choices = choices


class WidgetThemeAdmin(ModelAdmin):

    form = WidgetThemeForm

    list_display = ('__str__', 'widget_class')

    list_filter = ('widget_class',)


admin.site.register(WidgetTheme, WidgetThemeAdmin)


class PageThemeAdmin(ModelAdmin):

    pass

admin.site.register(PageTheme, PageThemeAdmin)
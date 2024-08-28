from django.contrib import admin
from .models import Dictionary, DictionaryVersion, DictionaryElement


class DictionaryVersionInline(admin.TabularInline):
    model = DictionaryVersion
    extra = 1


class DictionaryElementInline(admin.TabularInline):
    model = DictionaryElement
    extra = 1


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    inlines = [DictionaryVersionInline]


@admin.register(DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin):
    list_display = ('dictionary', 'version', 'start_date')
    search_fields = ('version',)
    list_filter = ('dictionary', 'start_date')
    inlines = [DictionaryElementInline]


@admin.register(DictionaryElement)
class DictionaryElementAdmin(admin.ModelAdmin):
    list_display = ('version', 'code', 'value')
    search_fields = ('code', 'value')
    list_filter = ('version__dictionary', 'version')

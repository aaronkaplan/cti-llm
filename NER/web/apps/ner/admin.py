from django.contrib import admin
from .models import InputText, Metadata, Output

class MetadataInline(admin.StackedInline):
    model = Metadata
    extra = 0

class OutputInline(admin.TabularInline):
    model = Output
    extra = 0

class InputTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_text', 'created_at')
    inlines = [MetadataInline, OutputInline]

admin.site.register(InputText, InputTextAdmin)

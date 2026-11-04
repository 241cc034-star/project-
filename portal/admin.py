
from django.contrib import admin
from .models import Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'uploaded_by',
        'status',
        'uploaded_at'
    )

    list_filter = ('status',)

    search_fields = (
        'title',
        'uploaded_by__username'
    )
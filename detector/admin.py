from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date', 'is_fake')  # Display key fields
    list_filter = ('is_fake', 'subject', 'date')  # Filters for easy navigation
    search_fields = ('title', 'text', 'subject')  # Search by title, text, and subject
    ordering = ('-date',)  # Order by most recent articles first
    readonly_fields = ('is_fake',)  # Prevent manual changes to classification
    date_hierarchy = 'date'  # Enables a date-based drill-down navigation

    def save_model(self, request, obj, form, change):
        """Automatically classify news before saving if it's new or text changes."""
        if not obj.pk or 'text' in form.changed_data:
            obj.classify_news()
        super().save_model(request, obj, form, change)

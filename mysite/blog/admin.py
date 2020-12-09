from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'was_published_recently')
    list_filter=['pub_date']
    search_fields = ['title', 'contents']

    fieldsets = [
        (None,      {'fields': ['title', 'contents']}),
    ]

admin.site.register(Post, PostAdmin)
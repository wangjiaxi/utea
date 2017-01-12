from django.contrib import admin
from .models import Source, PostList, Post


class PostListAdmin(admin.ModelAdmin):
    list_display = ["title", "article_type", "category", "_id", "source"]
    list_filter = ["source"]
    search_fields = ["title", "category"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "article_type", "category", "_id", "source"]
    list_filter = ["source"]
    search_fields = ["title", "category", "content"]


admin.site.register(Source)
admin.site.register(Post, PostAdmin)
admin.site.register(PostList, PostListAdmin)

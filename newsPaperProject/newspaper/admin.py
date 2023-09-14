from django.contrib import admin
from .models import Author, Category, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'rating')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post_type', 'title', 'text', 'get_category', 'data_post_creation')
    list_display_links = ('id', 'author', 'title')
    search_fields = ('id', 'title')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    # list_display_links = ('name')
    search_fields = ('id', 'name')



admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
# admin.site.unregister(Post)

# Register your models here.

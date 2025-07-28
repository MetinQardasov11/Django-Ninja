from django.contrib import admin
from .models import Blog, Category

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',)
    search_fields = ('name', 'description')
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
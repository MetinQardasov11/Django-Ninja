from ninja import NinjaAPI
from .models import Blog, Category
from .schemas import BlogSchema, CategorySchema
from django.shortcuts import get_object_or_404

api = NinjaAPI()


@api.get("/categories", response=list[CategorySchema])
def list_categories(request):
    return Category.objects.all()


@api.get("/blogs", response=list[BlogSchema])
def list_blogs(request):
    return Blog.objects.all()


@api.get("/blogs/{slug}", response=BlogSchema)
def get_blog(request, slug: str):
    blog = get_object_or_404(Blog, slug=slug)
    return blog
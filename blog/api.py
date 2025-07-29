from ninja import NinjaAPI
from .models import Blog, Category
from .schemas import (
    BlogSchema,
    CategorySchema,
    Error,
    CategoryCreateSchema,
)
from django.shortcuts import get_object_or_404

api = NinjaAPI()


@api.get("/categories", response=list[CategorySchema])
def list_categories(request):
    return Category.objects.all()


@api.post('/categories', response={200: CategorySchema, 404: Error})
def create_category(request, category: CategoryCreateSchema):
    if Category.objects.filter(name=category.name).exists():
        return 404, {"message": "Category already exists"}

    category_data = category.model_dump()
    category_model = Category.objects.create(**category_data)
    return category_model


@api.get('/categories/{category_id}', response=CategorySchema)
def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    if not category.name:
        return 404, {"message": "Category not found"}
    return category


@api.put('/categories/{category_id}', response={200: CategorySchema, 404: Error})
def update_category(request, category_id: int, data: CategoryCreateSchema):
    category = get_object_or_404(Category, id=category_id)
    if not category.name:
        return 404, {"message": "Category not found"}
    
    category.name = data.name
    category.save()
    return category


@api.delete("/categories/{category_id}", response={200: dict, 404: Error})
def delete_category(request, id: int):
    category = get_object_or_404(Category, id=id)
    if not category.name:
        return 404, {"message": "Category not found"}
    
    category.delete()
    return {"success": True}


@api.get("/blogs", response=list[BlogSchema])
def list_blogs(request):
    return Blog.objects.all()


@api.get("/blogs/{slug}", response=BlogSchema)
def get_blog(request, slug: str):
    blog = get_object_or_404(Blog, slug=slug)
    return blog
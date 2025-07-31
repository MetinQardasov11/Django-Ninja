from ninja import NinjaAPI
from .models import Blog, Category
from .schemas import (
    BlogSchema,
    CategorySchema,
    Error,
    CategoryCreateSchema,
    BlogCreateSchema,
    BlogCategoryPatch
)
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate, PageNumberPagination
from django.db.models import Q

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


@api.post('/blogs', response={200: BlogSchema, 404: Error})
def create_blog(request, blog: BlogCreateSchema):
    if blog.category_id:
        category_exists = Category.objects.filter(id=blog.category_id).exists()
        if not category_exists:
            return 404, {"message": "Category not found"}
        
    blog_data = blog.model_dump()
    blog_model = Blog.objects.create(**blog_data)
    return blog_model


@api.post('/blog/{slug}/set-category', response={200: BlogSchema, 404: Error})
def update_blog_category(request, blog_slug, category: BlogCategoryPatch):
    blog = get_object_or_404(Blog, slug=blog_slug)
    if category.category_id:
        category = get_object_or_404(Category, id=category.category_id) 
        blog.category = category
    else:
        blog.category = None

    blog.save()
    return blog


@api.put('/blogs/{slug}', response={200: BlogSchema, 404: Error})
def update_blog(request, slug: str, data: BlogCreateSchema):
    blog = get_object_or_404(Blog, slug=slug)

    blog.name = data.name
    blog.description = data.description

    if data.category_id is not None:
        blog.category = get_object_or_404(Category, id=data.category_id)
    else:
        blog.category = None

    blog.save()
    return blog


@api.delete('/blogs/{slug}', response={200: dict, 404: Error})
def delete_blog(request, slug: str):
    blog = get_object_or_404(Blog, slug=slug)
    if not blog.name:
        return 404, {"message": "Blog not found"}
    
    blog.delete()
    return blog


@api.get('/blogs/paginated', response=list[BlogSchema])
@paginate(PageNumberPagination, page_size=10)
def paginated_blogs(request):
    return Blog.objects.select_related("category").all()




@api.get("/blogs/search", response=list[BlogSchema])
def search_blogs(request, q: str):
    return Blog.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))



@api.get("/blogs/order", response=list[BlogSchema])
def order_blogs(request, order_by: str = "name"):
    return Blog.objects.all().order_by(order_by)

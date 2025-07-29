from ninja import ModelSchema, Schema
from .models import Category, Blog

class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('id', 'name')
        
        
class BlogSchema(ModelSchema):
    category: CategorySchema | None = None
    
    class Meta:
        model = Blog
        fields = ('id', 'name', 'slug', 'category', 'description')


class Error(Schema):
    message: str
        
    
class CategoryCreateSchema(Schema):
    name: str
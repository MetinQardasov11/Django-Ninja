from ninja import ModelSchema
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
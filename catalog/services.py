from .models import Category, Product


class CategoryService:
    """Business logic for Category operations."""
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    @staticmethod
    def get_category_by_id(category_id):
        return Category.objects.get(id=category_id)
    
    @staticmethod
    def create_category(data):
        return Category.objects.create(**data)
    
    @staticmethod
    def update_category(category, data):
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category
    
    @staticmethod
    def delete_category(category):
        category.delete()


class ProductService:
    """Business logic for Product operations."""
    
    @staticmethod
    def get_all_products():
        return Product.objects.select_related('category').all()
    
    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.select_related('category').get(id=product_id)
    
    @staticmethod
    def create_product(data):
        return Product.objects.create(**data)
    
    @staticmethod
    def update_product(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product
    
    @staticmethod
    def delete_product(product):
        product.delete()
    
    @staticmethod
    def get_products_by_category(category_id):
        return Product.objects.filter(category_id=category_id)
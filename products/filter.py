from django_filters import FilterSet, NumberFilter
from products.models import Product, Review

class ProductFilter(FilterSet):
    price_min = NumberFilter('price', lookup_expr='gte')
    price_max = NumberFilter('price', lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['categories', 'price_min', 'price_max']
        
class ReviewFilter(FilterSet):
    rating_min = NumberFilter('rating', lookup_expr='gte')
    rating_max = NumberFilter('rating', lookup_expr='lte')
    
    class Meta:
        model = Review
        fields = ['rating_min', 'rating_max']
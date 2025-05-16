from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter, DefaultRouter
from products.views import (ProductViewSet,
                            ReviewViewSet,
                            CartViewSet,
                            CartItemViewSet,
                            ProductTagListViewSet,
                            ProductImageViewSet,
                            FavoriteProductViewSet)

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart', CartViewSet)
router.register('cart_item', CartItemViewSet)
router.register('tags', ProductTagListViewSet)
router.register('favorite_products', FavoriteProductViewSet)

products_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
products_router.register('images', ProductImageViewSet, basename='product_images')
products_router.register('reviews', ReviewViewSet, basename='product_reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
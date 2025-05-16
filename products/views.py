from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError 
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from products.models import Product, Review, Cart, CartItem, ProductTag, FavoriteProduct, ProductImage
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, ProductTagSerializer, FavoriteProductSerializer, ProductImageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from products.pagination import ProductPagination
from products.filter import ProductFilter, ReviewFilter

class ProductViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'])
    def myproducts(self, request):
        my_product = Product.objects.filter(user=self.request.user)
        serializer = self.get_serializer(my_product, many=True)
        return Response(serializer.data)
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
    def get_queryset(self):
        queryset = self.queryset.filter(product__id=self.kwargs['product_pk'])
        return queryset
    
    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied('JUST NO')
        serializer.save()
        
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('JUST NO')
        instance.delete()
        
    
class FavoriteProductViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
class CartViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied('NET')
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied('NET')
        serializer.save()

class ProductTagListViewSet(ListModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]
    
class ProductImageViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(product__id=self.kwargs.get('product_id'))
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
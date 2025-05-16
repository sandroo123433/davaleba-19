from django.core.validators import ValidationError
from PIL import Image
from django.apps import apps

def validate_image_size(image):
    file_size = image.size
    limit = 5
    if file_size > limit * 1024 * 1024:
        raise ValidationError(f"So big")
    
def validate_image_dimensions(image):
    img = Image.open(image)
    min_width, min_height = 300, 300
    max_width, max_height = 4000, 4000

    width, height = img.size

    if width < min_width or height < min_height:
        raise ValidationError(f"So small")
    
    if width > max_width or height > max_height:
        raise ValidationError(f"So big")
    
def validate_image_count(product_id):
    ProductImage = apps.get_model('products', 'ProductImage')
    max_images = 5
    if ProductImage.objects.filter(product_id=product_id).count() >= max_images:
        raise ValidationError(f"SO many")
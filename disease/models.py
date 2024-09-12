from django.db import models
from config.models import BasedModel
from users.models import User

class ProductImage(BasedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at} by {self.user.email}"
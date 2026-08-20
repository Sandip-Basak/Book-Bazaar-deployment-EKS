from django.db import models
from django.contrib.auth.models import User
from store.models import Book
import uuid

def user_image(instance, filename):
    extension = filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"static/images/user/{unique_filename}"

# Create your models here.
class User_Data(models.Model):
    user=models.ForeignKey(User, unique=True, on_delete=models.CASCADE, related_name='user', verbose_name='Name')
    phone=models.DecimalField(max_digits=10,decimal_places=0,null=True)
    address=models.TextField(null=True)
    profile_photo=models.FileField(upload_to=user_image,default="static/images/media/default_user.png")

    def __str__(self):
        return f"Username:{self.user.username}"

class Wishlist(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE,related_name='book_wishlist',verbose_name='Book')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlist', verbose_name='Name')

    def __str__(self):
        return f"{self.user.username}-{self.book.name}"
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart', verbose_name='Name')
    book=models.ForeignKey(Book, on_delete=models.CASCADE,related_name='book_cart',verbose_name='Book')

    def __str__(self):
        return f"{self.user.username}-{self.book.name}"
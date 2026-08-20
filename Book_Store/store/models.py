from django.db import models
from django.contrib.auth.models import User
import uuid


# Generate unique file path for images
def book_image(instance, filename):
    extension = filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"static/images/book/{unique_filename}"

# Create your models here.
class Book(models.Model):
    bid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    author=models.CharField(max_length=300)
    publisher=models.CharField(max_length=400)
    date=models.DateField(verbose_name='Publish Date')
    summary=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=0)
    image=models.FileField(upload_to=book_image)

    def __str__(self):
        return f"Book ID:{self.bid} Name:{self.name}"
    
class Inventory(models.Model):
    book=models.ForeignKey(Book,unique=True , on_delete=models.CASCADE,related_name='book',verbose_name='Book')
    quantity=models.DecimalField(max_digits=10,decimal_places=0)
    sales=models.DecimalField(max_digits=10,decimal_places=0)

    def __str__(self):
        return f"Book ID:{self.book.bid}  Name:{self.book.name}  Quantity:{self.quantity}"
    
class Orders(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', verbose_name='Name')
    book=models.ForeignKey(Book, on_delete=models.CASCADE,related_name='book_order',verbose_name='Book')
    date=models.DateField(verbose_name='Order Date')

    def __str__(self):
        return f"{self.user.username}-{self.book.name}({self.date})"
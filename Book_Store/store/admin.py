from django.contrib import admin
from store.models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Inventory)
admin.site.register(Orders)
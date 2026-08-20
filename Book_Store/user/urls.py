from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.profile,name="home"),
    path('signout', views.signout,name="signout"),
    path('wishlist', views.wishlist,name="wishlist"),
    path('cart', views.cart,name="cart"),
    path('purchase', views.purchase,name="purchase"),
    path('orders', views.orders,name="orders"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
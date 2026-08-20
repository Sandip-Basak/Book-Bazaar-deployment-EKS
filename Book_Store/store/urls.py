from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name="home"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('book/<int:id>', views.product, name="product"),
    path('store', views.store, name="store"),
    path('store/<str:type>', views.store, name="store"),
    path('wishlist/<str:type>/<int:id>', views.update_wishlist, name="wishlist"),
    path('cart/<str:type>/<int:id>', views.update_cart, name="cart"),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
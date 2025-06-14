
from django.contrib import admin
from django.urls import include, path
from . import views
from safi import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('boutique/', include('store.urls')),
    path('carts/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

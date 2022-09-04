from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api.accounts import views as account_views

routers = DefaultRouter()

routers.register("accounts", account_views.UserViewSet, basename="accounts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-v1/", include(routers.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

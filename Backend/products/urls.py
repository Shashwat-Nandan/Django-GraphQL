from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, StoreViewSet

router = SimpleRouter()
router.register("products", ProductViewSet, basename='products')
router.register("", StoreViewSet, basename='stores')

urlpatterns = router.urls

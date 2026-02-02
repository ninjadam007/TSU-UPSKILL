from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, LocationCategoryViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'location-categories', LocationCategoryViewSet, basename='location-category')

urlpatterns = router.urls

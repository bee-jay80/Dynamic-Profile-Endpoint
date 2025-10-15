from django.urls import path
from get_user.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'me', UserViewSet, basename='me')

urlpatterns = router.urls
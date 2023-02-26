from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'product', views.ProductViewSet)

urlpatterns = router.urls
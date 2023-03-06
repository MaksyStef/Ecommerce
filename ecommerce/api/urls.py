from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'knife', views.KnifeProductView)
router.register(r'melee', views.MeleeProductView)
router.register(r'souvenir', views.SouvenirProductView)
router.register(r'flashlight', views.FlashlightProductView)
router.register(r'accompanying', views.AccompanyingProductView)

urlpatterns = router.urls
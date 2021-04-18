from rest_framework import routers

from menus.views import DishViewSet, MealViewSet, MenuViewset, OrderViewset

router = routers.DefaultRouter()
router.register(r"dishes", DishViewSet)
router.register(r"meals", MealViewSet)
router.register(r"menus", MenuViewset)
router.register(r"orders", OrderViewset)

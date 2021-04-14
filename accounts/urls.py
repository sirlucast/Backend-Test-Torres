from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import CustomObtainTokenPairView

urlpatterns = [
    path("api/token/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

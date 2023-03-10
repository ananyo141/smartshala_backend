from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from smartshala.core.views import UserListView

urlpatterns = [
    path("grader/", include("smartshala.grader_app.urls")),
    path("test/", include("smartshala.test_app.urls")),
    path("school/", include("smartshala.school_app.urls")),
    path("user/", UserListView.as_view(), name="user-list"),
    path(
        "auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

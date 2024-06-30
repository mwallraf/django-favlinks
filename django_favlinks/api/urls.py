from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"bookmarks", views.BookmarkViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("accounts/", include("django.contrib.auth.urls")),
]

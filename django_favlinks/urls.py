from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookmarkListView.as_view(), name="list_bookmark"),
    path(
        "<int:pk>/",
        views.BookmarkDetailView.as_view(),
        name="detail_bookmark",
    ),
    path("add/", views.BookmarkCreateView.as_view(), name="add_bookmark"),
    path("<int:pk>/update/", views.BookmarkUpdateView.as_view(), name="edit_bookmark"),
    path(
        "<int:pk>/delete/", views.BookmarkDeleteView.as_view(), name="delete_bookmark"
    ),
    path("<int:pk>/publish/", views.publish_bookmark, name="publish_bookmark"),
    path("<int:pk>/goto-bookmark/", views.goto_bookmark, name="goto_bookmark"),
    path("<int:pk>/favorite/", views.favorite_bookmark, name="favorite_bookmark"),
    path("export/", views.export_bookmarks, name="export_bookmarks"),
    path("import/", views.import_bookmarks, name="import_bookmarks"),
]

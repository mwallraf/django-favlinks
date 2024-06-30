from django.contrib import admin
from .models import Bookmark, Favorite, UserClickCount


# Register your models here.
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "owner", "is_private", "global_click_count")
    search_fields = ("title", "url", "tags")
    list_filter = ("is_private", "owner")
    ordering = ("-global_click_count",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "bookmark")
    search_fields = ("user__username", "bookmark__title")
    list_filter = ("user", "bookmark")


@admin.register(UserClickCount)
class UserClickCountAdmin(admin.ModelAdmin):
    list_display = ("user", "bookmark", "click_count")
    search_fields = ("user__username", "bookmark__title")
    list_filter = ("user", "bookmark")

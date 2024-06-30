from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Bookmark, UserClickCount, Favorite
import json
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.db.models import (
    Q,
    F,
    ObjectDoesNotExist,
    IntegerField,
    OuterRef,
)  # Import the Q object from models
from .forms import BookmarkForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BookmarkListView(ListView):
    model = Bookmark
    template_name = "favlinks/bookmark_list.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        """Get the queryset for this view.

        Authenticated users can see their own bookmarks and public bookmarks.
        Guest users can only see public bookmarks.

        Search queries are supported and search is performed on title, short description and tags.
        We can have multiple search queries separated by commas.

        Bookmark tags are stored as a comma-separated string in the database.

        Bookmarks are ordered by the number of clicks in descending order. If a bookmark
        has private clicks then the number of private clicks is used for ordering, otherwise
        the global click count is used.
        """
        if self.request.user.is_authenticated:
            bookmarks = Bookmark.objects.filter(
                Q(owner=self.request.user) | Q(is_private=False)
            ).distinct()
        else:
            bookmarks = Bookmark.objects.filter(is_private=False)

        search_queries = [
            q for q in self.request.GET.getlist("q") for q in q.split(",")
        ]
        if search_queries:
            query = None
            for q in search_queries:
                if not q:
                    continue
                if not query:
                    query = Q()
                query |= (
                    Q(title__icontains=q)
                    | Q(description__icontains=q)
                    | Q(tags__name__icontains=q)
                )
            bookmarks = bookmarks if not query else bookmarks.filter(query)
        # Annotate each bookmark if it is a favorite of the current user
        bookmarks = bookmarks.annotate(
            is_favorite=Coalesce(
                (
                    Favorite.objects.filter(
                        user=self.request.user, bookmark_id=OuterRef("pk")
                    ).values("id")[:1]
                    if self.request.user.is_authenticated
                    else None
                ),
                None,
                output_field=IntegerField(),
            )
        )

        # Annotate each bookmark with a 'user_click_count' or fall back to 'global_click_count' if 'user_click_count' does not exist
        bookmarks = bookmarks.annotate(
            custom_click_count=Coalesce(
                # Try to get the user-specific click count first
                (
                    UserClickCount.objects.filter(
                        user=self.request.user, bookmark_id=OuterRef("pk")
                    ).values("click_count")[:1]
                    if self.request.user.is_authenticated
                    else None
                ),
                # Fall back to the global click count if no user-specific count is found
                "global_click_count",
                output_field=IntegerField(),
            )
        )

        # Order the bookmarks by the custom click count
        bookmarks = bookmarks.order_by("-is_favorite", "-custom_click_count")

        bookmarks = bookmarks.prefetch_related("tags")

        return bookmarks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BookmarkForm()
        context["db_field_names"] = [
            field.name for field in self.model._meta.get_fields()
        ]

        return context


class BookmarkDetailView(DetailView):
    model = Bookmark
    # template_name = "favlinks/bookmark_detail.html"


class BookmarkCreateView(CreateView):
    model = Bookmark
    form_class = BookmarkForm
    # template_name = "favlinks/list.html"
    success_url = reverse_lazy("list_bookmark")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    form_class = BookmarkForm
    # template_name = "favlinks/bookmark_create.html"
    success_url = reverse_lazy("list_bookmark")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    # template_name = "favlinks/bookmark_confirm_delete.html"
    success_url = reverse_lazy("list_bookmark")


def bookmark_detail(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if request.user.is_authenticated:
        user_click, created = UserClickCount.objects.get_or_create(
            user=request.user, bookmark=bookmark
        )
        user_click.click_count += 1
        user_click.save()
    else:
        bookmark.global_click_count += 1
        bookmark.save()
    return render(request, "favlinks/bookmark_detail.html", {"bookmark": bookmark})


@login_required
def publish_bookmark(request, pk):
    bookmark = get_object_or_404(Bookmark, id=pk)
    if request.method == "POST":
        bookmark.is_private = False
        bookmark.save()
        return redirect(
            "list_bookmark"
        )  # Redirect to your bookmarks list or any appropriate page
    return redirect("list_bookmark")


def goto_bookmark(request, pk):
    """Opens a bookmark in a new tab and updates the click count."""
    bookmark = get_object_or_404(Bookmark, id=pk)
    if bookmark:
        # update global click count
        bookmark.global_click_count = F("global_click_count") + 1
        bookmark.save()

        # Update per-user click count
        if request.user.is_authenticated:
            try:
                user_click_count = UserClickCount.objects.get(
                    user=request.user,
                    bookmark=bookmark,
                )
                user_click_count.click_count = F("click_count") + 1
            except ObjectDoesNotExist:
                user_click_count = UserClickCount(
                    user=request.user,
                    bookmark=bookmark,
                    click_count=1,
                )
            user_click_count.save()

        return HttpResponseRedirect(bookmark.url)
    return redirect("list_bookmark")


@login_required
def favorite_bookmark(request, pk):
    """Marks a bookmark as favorite or unfavorite."""
    bookmark = get_object_or_404(Bookmark, id=pk)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, bookmark=bookmark
    )
    if not created:
        favorite.delete()
    return redirect("list_bookmark")


@login_required
def export_bookmarks(request):
    bookmarks = Bookmark.objects.filter(owner=request.user)
    data = [
        {
            "url": bm.url,
            "title": bm.title,
            "description": bm.description,
            "tags": bm.tags,
        }
        for bm in bookmarks
    ]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def import_bookmarks(request):
    bookmarks_data = json.loads(request.body)
    for bm_data in bookmarks_data:
        Bookmark.objects.create(
            url=bm_data["url"],
            title=bm_data["title"],
            description=bm_data["description"],
            tags=bm_data["tags"],
            owner=request.user,
        )
    return HttpResponse(status=204)

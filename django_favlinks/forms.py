from django import forms
from .models import Bookmark


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = [
            "url",
            "title",
            "description",
            "is_private",
            "screenshot",
            "tags",
        ]

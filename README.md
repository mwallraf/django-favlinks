# python-favlinks

**python-favlinks** is a Django application designed to help you manage your favorite links or bookmarks efficiently. The app features a user-friendly interface and advanced functionality for sorting, previewing, and filtering bookmarks.

## Features

- **Single Page with Bookmark List**: View all your bookmarks on a single page, sorted by popularity (number of clicks).
- **Thumbnail Previews**: See a preview thumbnail of each bookmarked website.
- **Tagging**: Add tags to your bookmarks for better organization and retrieval.
- **Filtering**: Easily filter bookmarks by tags, title, or description.

### User Access

#### Guest Users (Not Authenticated)
- View URLs that are visible to everyone.

#### Authenticated Users
- View URLs that are visible to everyone.
- Create private bookmarks, visible only to the user.
- Mark bookmarks as favorite to always keep them on top.
- Publish private bookmarks to make them available for everyone.
- Bookmarks are sorted by the number of clicks by the user.

## Installation

1. Install the package via pip:
    ```bash
    pip install python-favlinks
    ```

2. Add required apps to your `INSTALLED_APPS` in `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'rest_framework',
        'taggit',
        'crispy_forms',
        'crispy_bootstrap5',
        'favlinks',
    ]
    ```

3. Set the crispy template pack in your `settings.py`:
    ```python
    CRISPY_TEMPLATE_PACK = 'bootstrap5'
    ```

4. Set the static and media file location in you `settings.py`:
    ```python
    STATIC_URL = "static/"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    ```


5. Include the `favlinks` URL configuration in your `urls.py`:
    ```python
    from django.urls import path, include

    urlpatterns = [
        ...
        path("favlinks/", include("django_favlinks.urls")),
        path("api/favlinks/", include("django_favlinks.api.urls")),
    ]
    ```

6. Run the migrations to create the necessary database tables:
    ```bash
    python manage.py migrate
    ```

## Usage

Once installed, you can access the bookmarks management interface at `/favlinks/`. Here, you can view, add, edit, and filter your bookmarks.

### Adding Bookmarks

You can only add bookmarks if you are logged in.

### Filtering Bookmarks

Use the filter options on the main bookmarks page to narrow down your bookmarks by tags, title, or description.

## Styling

This project uses basic Bootstrap 5 styling. Ensure you have Bootstrap 5 included in your base template.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more information and detailed documentation, visit the [project's GitHub page](https://github.com/mwallraf/python-favlinks).


from django.shortcuts import render
from feed.models import SiteSettings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # 1. Always allow access to the admin panel (with or without trailing slash)
        if path == "/admin" or path.startswith("/admin/"):
            return self.get_response(request)

        # 2. Always allow static and media assets
        if path.startswith("/static/") or path.startswith("/media/") or path == "/favicon.ico":
            return self.get_response(request)

        # 3. Allow logged-in staff and superusers to bypass maintenance mode
        if hasattr(request, "user") and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return self.get_response(request)

        try:
            # Get the first SiteSettings object
            settings = SiteSettings.objects.first()
            if settings and settings.is_maintenance_mode:
                return render(request, "maintenance.html", status=503)
        except Exception:
            # If the database table doesn't exist yet, just continue
            pass

        return self.get_response(request)

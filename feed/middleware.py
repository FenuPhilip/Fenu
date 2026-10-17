from django.shortcuts import render


class MaintenanceModeMiddleware:
    """
    Shows maintenance.html (HTTP 503) for all public requests when
    SiteSettings.is_maintenance_mode is True.

    Paths that are ALWAYS allowed regardless of maintenance mode:
      • /admin/  and  /admin  — Django admin panel
      • /static/ — static assets (CSS, JS, images)
      • /media/  — uploaded media files
      • /favicon.ico

    Note: staff/superuser bypass is intentionally removed.
    The admin panel is always reachable at /admin/ — that's the only
    control surface that should be exempt.
    """

    ALWAYS_ALLOWED_PREFIXES = (
        "/admin/",
        "/static/",
        "/media/",
    )
    ALWAYS_ALLOWED_EXACT = {"/admin", "/favicon.ico"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Fast-path: always allow admin + assets
        if path in self.ALWAYS_ALLOWED_EXACT:
            return self.get_response(request)

        for prefix in self.ALWAYS_ALLOWED_PREFIXES:
            if path.startswith(prefix):
                return self.get_response(request)

        # Check maintenance mode
        if self._is_maintenance():
            return render(request, "maintenance.html", status=503)

        return self.get_response(request)

    @staticmethod
    def _is_maintenance() -> bool:
        """
        Returns True if maintenance mode is currently active.
        Catches all DB / app-startup exceptions so a missing table
        never breaks the site.
        """
        try:
            from feed.models import SiteSettings
            solo = SiteSettings.objects.filter(pk=1).first()
            return bool(solo and solo.is_maintenance_mode)
        except Exception:
            return False

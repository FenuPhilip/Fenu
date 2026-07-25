from django.shortcuts import render
from feed.models import SiteSettings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Always allow access to the admin panel
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        try:
            # Get the first SiteSettings object
            settings = SiteSettings.objects.first()
            if settings and settings.is_maintenance_mode:
                return render(request, 'maintenance.html', status=503)
        except Exception:
            # If the database table doesn't exist yet, just continue
            pass
            
        return self.get_response(request)

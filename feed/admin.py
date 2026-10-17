from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Profile, Post, Contact, Skill, SiteSettings, SiteStat


# ---------------------------------------------------------------------------
# SiteStat
# ---------------------------------------------------------------------------

@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ("id", "visits")


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role")


# ---------------------------------------------------------------------------
# Post
# ---------------------------------------------------------------------------

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("post_type", "caption", "created_at", "is_published", "is_featured")
    list_filter = ("post_type", "is_published", "is_featured")


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    readonly_fields = ("name", "email", "phone", "message", "created_at")


# ---------------------------------------------------------------------------
# Skill
# ---------------------------------------------------------------------------

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "category")


# ---------------------------------------------------------------------------
# SiteSettings  ──  Singleton admin with a one-click toggle
# ---------------------------------------------------------------------------

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Singleton admin for SiteSettings.

    • Prevents adding a second instance.
    • Provides a big one-click "Toggle Maintenance Mode" button.
    • Shows a coloured status badge in the list view.
    """

    list_display = ("maintenance_status_badge", "toggle_button")
    readonly_fields = ("maintenance_status_badge",)

    # ------------------------------------------------------------------
    # Singleton guard: redirect "Add" to the one existing instance
    # ------------------------------------------------------------------

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Never delete the singleton

    def changelist_view(self, request, extra_context=None):
        """Skip the list; go straight to the change form."""
        solo = SiteSettings.get_solo()
        return redirect(
            f"/admin/feed/sitesettings/{solo.pk}/change/"
        )

    # ------------------------------------------------------------------
    # Custom URL for the toggle action
    # ------------------------------------------------------------------

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "toggle-maintenance/",
                self.admin_site.admin_view(self.toggle_maintenance),
                name="sitesettings_toggle_maintenance",
            )
        ]
        return custom + urls

    def toggle_maintenance(self, request):
        """Flip is_maintenance_mode and redirect back to the settings page."""
        solo = SiteSettings.get_solo()
        solo.is_maintenance_mode = not solo.is_maintenance_mode
        solo.save()
        status = "ON 🔴" if solo.is_maintenance_mode else "OFF 🟢"
        messages.success(request, f"Maintenance mode turned {status}")
        return redirect("/admin/feed/sitesettings/")

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    @admin.display(description="Status")
    def maintenance_status_badge(self, obj):
        if obj.is_maintenance_mode:
            return format_html(
                '<span style="'
                "background:#ef4444;color:#fff;padding:4px 12px;"
                "border-radius:9999px;font-weight:600;font-size:13px;"
                '">\u26a0\ufe0f Maintenance Mode ON</span>'
            )
        return format_html(
            '<span style="'
            "background:#22c55e;color:#fff;padding:4px 12px;"
            "border-radius:9999px;font-weight:600;font-size:13px;"
            '">\u2705 Site is Live</span>'
        )

    @admin.display(description="Action")
    def toggle_button(self, obj):
        if obj.is_maintenance_mode:
            label = "Turn OFF Maintenance"
            color = "#22c55e"
        else:
            label = "Turn ON Maintenance"
            color = "#ef4444"

        return format_html(
            '<a href="/admin/feed/sitesettings/toggle-maintenance/" '
            'style="background:{};color:#fff;padding:6px 16px;border-radius:6px;'
            'text-decoration:none;font-weight:600;font-size:13px;" '
            'onclick="return confirm(\'Are you sure?\');">'
            "{}</a>",
            color,
            label,
        )

    # Keep the change form simple — just the boolean field + the badge
    fields = ("maintenance_status_badge", "is_maintenance_mode")

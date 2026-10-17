from django.core.management.base import BaseCommand
from feed.models import SiteSettings


class Command(BaseCommand):
    help = "Enable, disable, or check maintenance mode (usage: python manage.py maintenance [on|off|status])"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            nargs="?",
            default="status",
            choices=["on", "off", "status"],
            help="Action to perform: on, off, or status (default: status)",
        )

    def handle(self, *args, **options):
        action = options["action"]
        settings, _ = SiteSettings.objects.get_or_create(id=1)

        if action == "on":
            settings.is_maintenance_mode = True
            settings.save()
            self.stdout.write(self.style.SUCCESS("Maintenance mode is now ENABLED."))
        elif action == "off":
            settings.is_maintenance_mode = False
            settings.save()
            self.stdout.write(self.style.SUCCESS("Maintenance mode is now DISABLED."))
        else:
            status = "ENABLED" if settings.is_maintenance_mode else "DISABLED"
            style = self.style.WARNING if settings.is_maintenance_mode else self.style.SUCCESS
            self.stdout.write(style(f"Maintenance mode is currently {status}."))

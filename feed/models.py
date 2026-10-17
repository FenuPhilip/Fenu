from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    hero_title = models.CharField(
        max_length=200,
        default="Building systems, not just software."
    )

    hero_subtitle = models.CharField(
        max_length=300,
        default="Cybersecurity • Full-stack • Robotics"
    )

    def __str__(self):
        return self.name


class Post(models.Model):

    POST_TYPE_CHOICES = [
        ("project", "Project"),
        ("event", "Event"),
    ]

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default="project"
    )

    caption = models.TextField(blank=True)

    # Media uploads
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos/", blank=True, null=True)

    # External embeds (Instagram / YouTube / etc)
    external_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post_type.upper()} - {self.caption[:30]}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Skill(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=3)  # 1–5
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class SiteStat(models.Model):
    visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Visits: {self.visits}"


class SiteSettings(models.Model):
    """Singleton model – only one row (id=1) should ever exist."""

    is_maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="Maintenance Mode",
        help_text=(
            "When ON, the public site shows the maintenance page. "
            "The Django admin (/admin/) is never affected."
        ),
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        status = "🔴 MAINTENANCE ON" if self.is_maintenance_mode else "🟢 Site Live"
        return f"Global Site Settings — {status}"

    def save(self, *args, **kwargs):
        """Force singleton: always use pk=1."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Return the singleton instance, creating it if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
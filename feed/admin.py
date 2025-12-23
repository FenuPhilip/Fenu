from django.contrib import admin
from .models import Profile, Post, Contact, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("post_type", "caption", "created_at", "is_published")
    list_filter = ("post_type", "is_published")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "created_at")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "category")


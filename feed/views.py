from django.shortcuts import render
from .models import Profile, Post, Contact, Skill, SiteStat

VISIT_COOKIE_NAME = "visited_fenu"
VISIT_COOKIE_AGE = 60 * 60 * 24  # 24 hours


def home(request):
    # -------------------------
    # VISITOR COUNTER (SMART)
    # -------------------------
    stat, _ = SiteStat.objects.get_or_create(id=1)

    should_count = True

    # ❌ Do not count YOU (admin / logged-in superuser)
    if request.user.is_authenticated and request.user.is_superuser:
        should_count = False

    # ❌ Do not count repeat visits (24h cookie)
    if request.COOKIES.get(VISIT_COOKIE_NAME):
        should_count = False

    if should_count:
        stat.visits += 1
        stat.save()

    # -------------------------
    # CONTACT FORM
    # -------------------------
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone", ""),
            message=request.POST.get("message"),
        )

    # -------------------------
    # DATA
    # -------------------------
    profile = Profile.objects.first()
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    skills = Skill.objects.all()

    response = render(request, "home.html", {
        "profile": profile,
        "posts": posts,
        "skills": skills,
        "visits": stat.visits,
    })

    # -------------------------
    # SET COOKIE (24 HOURS)
    # -------------------------
    if should_count:
        response.set_cookie(
            VISIT_COOKIE_NAME,
            "yes",
            max_age=VISIT_COOKIE_AGE,
            httponly=True,
            samesite="Lax",
        )

    return response

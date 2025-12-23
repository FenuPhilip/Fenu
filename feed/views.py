from django.shortcuts import render
from .models import Profile, Post, Contact, Skill, SiteStat


def home(request):
    # ---- VISITOR COUNTER ----
    stat, _ = SiteStat.objects.get_or_create(id=1)
    stat.visits += 1
    stat.save()

    # ---- CONTACT FORM ----
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone", ""),
            message=request.POST.get("message"),
        )

    # ---- DATA ----
    profile = Profile.objects.first()
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    skills = Skill.objects.all()

    # ---- RENDER ----
    return render(request, "home.html", {
        "profile": profile,
        "posts": posts,
        "skills": skills,
        "visits": stat.visits,   # 👁 visitor count
    })

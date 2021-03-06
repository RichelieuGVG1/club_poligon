import random
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.http import HttpResponse
from auth.helpers import auth_required, set_session_cookie
from auth.models import Session
from club.exceptions import AccessDenied
from posts.models.post import Post
from users.models.user import User
from utils.strings import random_string


def reg(request):
    now = datetime.utcnow()
    email = request.GET.get("email") or ""
    if email:
        email = email.lower()
    user, _ = User.objects.get_or_create(
                email=email,
                defaults=dict(
                    membership_platform_type=User.MEMBERSHIP_PLATFORM_DIRECT,
                    full_name=email[:email.find("@")],
                    membership_started_at=now,
                    membership_expires_at=datetime(2122, 12, 21),
                    created_at=now,
                    updated_at=now,
                    moderation_status=User.MODERATION_STATUS_INTRO,
                ),
            )

    user.save()

    return render(request, "auth/email.html")
    




def join(request):
    if request.me:
        return redirect("profile", request.me.slug)

    return render(request, "auth/join.html")


def login(request):
    if request.me:
        return redirect("profile", request.me.slug)

    return render(request, "auth/login.html", {
        "goto": request.GET.get("goto"),
        "email": request.GET.get("email"),
    })


@auth_required
def logout(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    token = request.COOKIES.get("token")
    Session.objects.filter(token=token).delete()
    cache.delete(f"token:{token}:session")
    return redirect("index")


def debug_dev_login(request):
    if not (settings.DEBUG or settings.TESTS_RUN):
        raise AccessDenied(title="Куда лезешь, смертный? Тебе сюда нельзя")

    user, is_created = User.objects.get_or_create(
        slug="dev",
        defaults=dict(
            patreon_id="123456",
            membership_platform_type=User.MEMBERSHIP_PLATFORM_PATREON,
            email="dev@dev.dev",
            full_name="Главный разработчик",
            company="incmisis Club",
            position="Ген. директор",
            balance=10000,
            membership_started_at=datetime.utcnow(),
            membership_expires_at=datetime.utcnow() + timedelta(days=365 * 100),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_email_verified=True,
            moderation_status=User.MODERATION_STATUS_APPROVED,
            roles=["god"],
        ),
    )

    if is_created:
        Post.upsert_user_intro(user, "Очень плохое интро", is_visible=True)

    session = Session.create_for_user(user)

    return set_session_cookie(redirect("profile", user.slug), user, session)


def debug_random_login(request):
    if not (settings.DEBUG or settings.TESTS_RUN):
        raise AccessDenied(title="Куда лезешь, смертный? Тебе сюда нельзя")

    slug = "random_" + random_string()
    user, is_created = User.objects.get_or_create(
        slug=slug,
        defaults=dict(
            patreon_id=random_string(),
            membership_platform_type=User.MEMBERSHIP_PLATFORM_PATREON,
            email=slug + "@random.dev",
            full_name="%s %d y.o. Developer" % (random.choice(["Максим", "Олег"]), random.randint(18, 101)),
            company="Acme Corp.",
            position=random.choice(["Подниматель пингвинов", "Опускатель серверов", "Коллектор пивных бутылок"]),
            balance=10000,
            membership_started_at=datetime.utcnow(),
            membership_expires_at=datetime.utcnow() + timedelta(days=365 * 100),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_email_verified=True,
            moderation_status=User.MODERATION_STATUS_APPROVED,
        ),
    )

    if is_created:
        Post.upsert_user_intro(user, "Хорошее интро, мы его одобрили! Так держать, боец!", is_visible=True)

    session = Session.create_for_user(user)

    return set_session_cookie(redirect("profile", user.slug), user, session)

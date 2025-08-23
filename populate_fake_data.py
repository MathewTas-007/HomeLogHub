import os
import django
import random
from django.db.utils import IntegrityError

# =========================
# 1️⃣ Setup Django properly
# =========================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hlh_project.settings")
django.setup()

# =========================
# 2️⃣ Import models AFTER setup
# =========================
from django.contrib.auth import get_user_model
from home_logs.models import LogEntry, Tag

User = get_user_model()

# =========================
# 3️⃣ Create superuser safely
# =========================
superuser_username = "kazi_admin"
superuser_email = "kazi_admin@example.com"
superuser_password = "SuperStrong123"

su, created = User.objects.get_or_create(
    username=superuser_username,
    defaults={"email": superuser_email}
)
if created:
    su.set_password(superuser_password)
    su.is_superuser = True
    su.is_staff = True
    su.save()
    print(f"🛡️ Superuser created: {su.username}")
else:
    print(f"🛡️ Superuser exists: {su.username}")

# =========================
# 4️⃣ Create test users
# =========================
users_data = [
    {"username": "TAS-001", "email": "tas001@example.com"},
    {"username": "TAS-002", "email": "tas002@example.com"},
    {"username": "TAS-003", "email": "tas003@example.com"},
]

for udata in users_data:
    try:
        user, created = User.objects.get_or_create(
            username=udata["username"],
            defaults={"email": udata["email"]}
        )
        if created:
            user.set_password("password123")
            user.save()
        print(f"✅ User: {user.username}")
    except IntegrityError:
        print(f"⚠️ User {udata['username']} already exists, skipping.")

# =========================
# 5️⃣ Create tags
# =========================
tags_list = ["system", "content", "login", "server", "app"]
tags_objects = []

for tname in tags_list:
    tag, _ = Tag.objects.get_or_create(name=tname, user=su)
    tags_objects.append(tag)
    print(f"🏷️ Tag: {tag.name}")

# =========================
# 6️⃣ Create logs
# =========================
log_titles = [
    "App-related improvements or fixes",
    "Unexpected issues or app crashes",
    "Content or file upload actions",
    "Login, signup, and password-related activities",
    "Events related to server or backend systems",
]

for user in User.objects.exclude(is_superuser=True):
    for title in log_titles:
        log, _ = LogEntry.objects.get_or_create(
            user=user,
            content=f"{title} - {user.username}",
            defaults={"mood": random.choice(["happy", "neutral", "sad"])}
        )
        # Assign 1-2 tags safely
        num_tags = min(len(tags_objects), random.randint(1, 2))
        assigned_tags = random.sample(tags_objects, k=num_tags)
        log.tags.set(assigned_tags)
        log.save()
        print(f"📝 Log: {log.content} | Tags: {[t.name for t in assigned_tags]}")

# =========================
# 7️⃣ Done!
# =========================
print("🔥 All fake users, logs, and tags populated!")
print(f"🛡️ Superuser credentials: {superuser_username} / {superuser_password}")

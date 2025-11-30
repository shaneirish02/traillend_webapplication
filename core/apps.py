from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        - Automatically create superuser (if env vars exist)
        - Automatically start the background scheduler loop
        """

        # ==============================
        # 1. Auto-create superuser
        # ==============================
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            try:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    print(f"✔ Superuser '{username}' created automatically.")
                else:
                    print(f"✔ Superuser '{username}' already exists.")
            except (OperationalError, ProgrammingError):
                # This happens before migrations; ignore safely
                pass

        # ==============================
        # 2. Start background scheduler
        # ==============================
        try:
            from core.scheduler import start_scheduler_loop
            start_scheduler_loop()
        except Exception as e:
            # Fail silently so app still loads
            print(f"[Scheduler Init Error] {e}")

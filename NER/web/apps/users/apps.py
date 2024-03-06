from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        try:
            import apps.users.signals  # noqa: F401
        except ImportError:
            pass

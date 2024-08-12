from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "A Demo for Django Custom commands"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS(
                f"Current PROJECT_RUNNING_ENV '{settings.PROJECT_RUNNING_ENV}'"
            )
        )
        self.stdout.write(self.style.SUCCESS("...checking admin config"))
        phone_number = settings.PROJECT_ADMIN_DETAIL

        is_project_admin_exist = User.objects.filter(
            phone_number=phone_number, is_staff=True, is_superuser=True
        ).exists()

        if is_project_admin_exist:
            self.stdout.write(self.style.SUCCESS("admin config already exists"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin config not found"))

            is_admin_user_exist = User.objects.filter(
                phone_number=phone_number
            ).exists()

            if is_admin_user_exist:
                self.stdout.write(self.style.WARNING("user already exist"))
            else:
                user = User.objects.create(
                    phone_number=phone_number,
                    is_staff=True,
                    is_superuser=True,
                )
                user.set_password(settings.PROJECT_ADMIN_DEFAULT_SECRET)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS("admin config applied successfully!")
                )

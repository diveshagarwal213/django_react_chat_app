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
                    first_name="admin",
                    last_name="admin",
                    phone_number=phone_number,
                    is_staff=True,
                    is_superuser=True,
                )
                user.set_password(settings.PROJECT_ADMIN_DEFAULT_SECRET)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS("admin config applied successfully!")
                )

        #
        demo_users = [
            {"first_name": "John", "last_name": "Doe", "phone_number": "+91720977989"},
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "phone_number": "+917809772989",
            },
            {
                "first_name": "Rahul",
                "last_name": "Sharma",
                "phone_number": "+917909772989",
            },
            {
                "first_name": "Maria",
                "last_name": "Garcia",
                "phone_number": "+918744964282",
            },
            {
                "first_name": "Chen",
                "last_name": "Wang",
                "phone_number": "+918474964282",
            },
        ]
        phone_numbers = [item["phone_number"] for item in demo_users]
        demo_user_exist = User.objects.filter(phone_number__in=phone_numbers).exists()
        if not demo_user_exist:
            self.stdout.write(self.style.SUCCESS("creating demo users..."))
            demo_users_objs = [User(**item) for item in demo_users]
            User.objects.bulk_create(demo_users_objs)
            self.stdout.write(self.style.SUCCESS("creating demo users created!"))
        else:
            self.stdout.write(self.style.SUCCESS("Demo Users exists!"))

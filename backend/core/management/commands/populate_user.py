from faker import Faker
from django.core.management import BaseCommand

from account.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        for x in range(30):
            user = CustomUser.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='',
                is_examiner=False
            )
            user.set_password('2468')
            user.save()

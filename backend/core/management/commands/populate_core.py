from django.core.management import BaseCommand
from faker import Faker
from random import randrange, choice
from core.models import Answer, Exam, Question, Result


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(30):
            exam = Exam.objects.create(
                title = faker.paragraph(),
                is_available = True,
                instructions = faker.text(),
            )
            for _ in range(50):
                Question.objects.create(
                    exam = exam,
                    exam_image = faker.image_url(),
                    question = faker.text(),
                    option1 = faker.text(),
                    option2 = faker.text(),
                    option3 = faker.text(),
                    option4 = faker.text(),
                    option5 = faker.text(),
                    answer = choice(['A', 'B', 'C', 'D', 'E']),
                )
            
            

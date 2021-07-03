from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


CHOICES = (
    ('A', 'option1'),
    ('B', 'option2'),
    ('C', 'option3'),
    ('D', 'option4'),
    ('E', 'option5'),
)


class Exam(models.Model):
    '''Database model for examination'''
    title = models.CharField(unique=True, max_length=255)
    is_available = models.BooleanField(default=False)
    duration = models.PositiveIntegerField('Time in seconds', default=60)
    instructions = models.TextField(default=' ')
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Result',
        related_name='exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def upload_image(instance, filename):
    return f"{instance.pk}/{filename}"


class Question(models.Model):
    '''Database model for question'''
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='questions')
    exam_image = models.ImageField(
        upload_to=upload_image, null=True, blank=True)
    question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    option5 = models.CharField(max_length=255, blank=True)
    answer = models.CharField(max_length=255, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def is_correct(self, option):
        return self.answer == option


class Result(models.Model):
    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_results')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='results')
    attempted = models.IntegerField(default=0)
    not_attempted = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    total_mark = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.exam} Result for {self.taker}, mark: {self.total_mark}"

    @property
    def score(self):
        return (self.correct_answers / (self.attempted + self.not_attempted)) * 100


class Answer(models.Model):
    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='user_answers')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='exam_answers')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    taker_choice = models.CharField(max_length=10, default='', choices=CHOICES)
    is_correct = models.BooleanField(default=False)

    def save(self) -> None:
        if not self.pk:
            self.is_correct = self.question.answer == self.taker_choice
        return super().save()


def post_save_answer_update_result(sender, instance, created, *args, **kwargs):
    '''Populate exact result instance as answers are saved'''
    if created:
        result = Result.objects.filter(
            taker=instance.taker, exam=instance.exam).first()
        if instance.taker_choice:
            if instance.is_correct:
                result.correct_answer += 1
            else:
                result.wrong_answer += 1
            result.attempted += 1
        else:
            result.not_attempted += 1
        result.save()

post_save.connect(post_save_answer_update_result, sender=Answer)

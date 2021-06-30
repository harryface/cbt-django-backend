from django.db import models
from django.conf import settings

# Create your models here.

CHOICES = (
    ('A', 'option1'),
    ('B', 'option2'),
    ('C', 'option3'),
    ('D', 'option4'),
    ('E', 'option5'),
)


def upload_image(instance, filename):
    return f"{instance.pk}/{filename}"


class Exam(models.Model):
    '''Database model for examination'''
    
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=False)
    duration = models.DurationField(default='00:00:00')
    instructions = models.TextField(default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Question(models.Model):
    '''Database model for question'''
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    exam_image = models.ImageField(upload_to=upload_image, null=True, blank=True, \
        height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    option5 = models.CharField(max_length=255, blank=True)
    answer = models.CharField(max_length=255, choices=CHOICES)

    def __str__(self):
        return self.text
    
    
class Result(models.Model):
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,\
        related_name='user_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_results')
    number_of_attempt = models.IntegerField(default=0)
    number_of_unattempt = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    total_mark = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.exam} Result for {self.taker}, mark: {self.total_mark}"
    
    
class Answer(models.Model):
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,\
        related_name='user_answers')
    result = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='result_answers')
    question = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='question_answers')
    taker_choice = models.CharField(max_length=10, choices=CHOICES)
    correct_choice = models.CharField(max_length=10, choices=CHOICES)
    
    
    
    
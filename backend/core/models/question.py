from django.db import models


def upload_image(instance, filename):
    return f"{instance.pk}/{filename}"


class Question(models.Model):
    '''Database model for question
    The answer should be a copy of the options. this would allow for randomization.'''
    exam = models.ForeignKey("core.Exam",
            on_delete=models.CASCADE, null=True, related_name='questions')
    image = models.ImageField(
        upload_to=upload_image, null=True, blank=True)
    question = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    option_5 = models.CharField(max_length=255, blank=True)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.id

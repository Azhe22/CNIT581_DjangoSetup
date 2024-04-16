from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Example(models.Model):
    # id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_examples')
    title = models.CharField(max_length=255)
    project_description = models.TextField()
    project_context = models.TextField()
    data_table_description = models.TextField()
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} by {self.creator.user.username}"


class Question(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()


class QuestionStep(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='steps')
    description = models.TextField()
    order = models.IntegerField(help_text="The order of the step within the question")

    class Meta:
        ordering = ['order']


class Review(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')


class ReviewStepResponse(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='step_responses')
    question_step = models.ForeignKey(QuestionStep, on_delete=models.CASCADE, related_name='review_responses')
    sql_statement = models.TextField()
    # Add more fields as necessary for step response


class Feedback(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='feedbacks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.CharField(max_length=50, choices=[
        ('completely_disagree', 'Completely Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('completely_agree', 'Completely Agree'),
    ])
    free_response = models.TextField(blank=True, null=True)


class AssignedReview(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='assigned_reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.example.title} assigned to {self.reviewer.user.username}"

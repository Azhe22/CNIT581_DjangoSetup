from django.contrib import admin
from .models import Profile, Example, Question, QuestionStep, Review, ReviewStepResponse, Feedback, AssignedReview
# Register your models here.
admin.site.register(Profile)
admin.site.register(Example)
admin.site.register(Question)
admin.site.register(QuestionStep)
admin.site.register(Review)
admin.site.register(ReviewStepResponse)
admin.site.register(Feedback)
admin.site.register(AssignedReview)



from django.urls import path

from .views import (
    CreateQuestionView,
)


app_name = 'question'
urlpatterns = [
    path('<int:course_id>/assignments/<int:assignment_id>/add-question/',
         CreateQuestionView.as_view(), name='create-assignment-question'),

    # path('<int:course_id>/assignments/<int:assignment_id>/submit/',
    #      SubmitView.as_view(), name='upload-solution'),
]

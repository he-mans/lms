from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView
)
from .forms import QuizCreationForm

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime
from django.shortcuts import reverse
# Create your views here.


class QuizCreationView(CreateView):
    form_class = QuizCreationForm
    template_name = 'quiz/create.html'

    def check_validity(self):
        course_id = self.kwargs.get('course_id')

        try:
            course = self.request.user.hosted_courses.get(id=course_id)
            if self.kwargs.get('course_type') != 'my-courses':
                raise Http404
        except ObjectDoesNotExist:
            raise Http404

        return course

    def get(self, request, *args, **kwargs):
        self.check_validity()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        course = self.check_validity()
        form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs.get('course_id')
        return context


class QuizListView(ListView):
    template_name = 'quiz/list.html'

    def get_queryset(self):
        course_type = self.kwargs.get('course_type')
        courseId = self.kwargs.get("course_id")
        if course_type == 'my-courses':
            return self.request.user.hosted_courses.get(id=courseId).quizzes.all().order_by('-date_created')
        elif course_type == 'enrolled-courses':
            return self.request.user.enrolled_courses.get(course__id=courseId).course.quizzes.all().order_by('-date_created')

    def get_context_data(self, **kwargs):
        course_type = self.kwargs.get('course_type')
        context = super().get_context_data(**kwargs)
        context['is_tutor'] = True if course_type == 'my-courses' else False
        context['course_type'] = course_type
        context['course_id'] = self.kwargs.get('course_id')
        return context


class QuizDetailView(DetailView):
    template_name = 'quiz/detail.html'

    def get_my_course_quiz(self, course_id, quiz_id):
        try:
            course = self.request.user.hosted_courses.get(id=course_id)
            return course.quizzes.get(id=quiz_id)
        except ObjectDoesNotExist:
            raise Http404

    def get_enrolled_course_quiz(self, course_id, quiz_id):
        try:
            course = self.request.user.enrolled_courses.get(
                course__id=course_id).course
            return course.quizzes.get(id=quiz_id)
        except ObjectDoesNotExist:
            raise Http404

    def get_object(self, queryset=None):
        course_id = self.kwargs.get('course_id')
        quiz_id = self.kwargs.get('quiz_id')
        course_type = self.kwargs.get('course_type')
        if course_type == 'my-courses':
            return self.get_my_course_quiz(course_id, quiz_id)
        elif course_type == 'enrolled-courses':
            return self.get_enrolled_course_quiz(course_id, quiz_id)

    def is_locked(self, object):
        current_datetime = datetime.now()
        if current_datetime.date() < object.quiz_date:
            return True
        if current_datetime.date() == object.quiz_date and current_datetime.time() < object.start_time:
            return True
        return False

    def is_ongoing(self, object):
        current_datetime = datetime.now()
        if current_datetime.date() == object.quiz_date and current_datetime.time() >= object.start_time and current_datetime.time() < object.end_time:
            return True
        else:
            return False

    def is_expired(self, object):
        current_datetime = datetime.now()
        if current_datetime.date() > object.quiz_date:
            return True
        if current_datetime.date() == object.quiz_date and current_datetime.time() > object.end_time:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_type = self.kwargs.get('course_type')
        # questions = context.get('object').questions.all()
        # context['questions'] = questions
        # context['question_count'] = questions.count()
        context['is_tutor'] = True if self.kwargs.get(
            'course_type') == 'my-courses' else False
        context['is_student'] = True if self.kwargs.get(
            'course_type') == 'enrolled-courses' else False
        context['course_type'] = course_type
        context['course_id'] = self.kwargs.get('course_id')
        context['locked'] = self.is_locked(context['object'])
        context['ongoing'] = self.is_ongoing(context['object'])
        context['expired'] = self.is_expired(context['object'])

        return context


class QuizUpdateView(UpdateView):
    template_name = 'quiz/update.html'
    form_class = QuizCreationForm

    def get_success_url(self):
        return reverse('quiz:detail', kwargs=self.kwargs)

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('course_type') != 'my-courses':
            raise Http404
        else:
            return super().get(request, *args, **kwargs)

    def get_my_course_quiz(self, course_id, quiz_id):
        try:
            course = self.request.user.hosted_courses.get(id=course_id)
            return course.quizzes.get(id=quiz_id)
        except ObjectDoesNotExist:
            raise Http404

    def get_object(self, queryset=None):
        course_id = self.kwargs.get('course_id')
        quiz_id = self.kwargs.get('quiz_id')
        course_type = self.kwargs.get('course_type')
        return self.get_my_course_quiz(course_id, quiz_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs.get('course_id')
        context['quiz_id'] = self.kwargs.get("quiz_id")
        return context

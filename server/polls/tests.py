from django.test import TestCase

import datetime
from django.utils import timezone

from polls.models import Question


class QuestionTests(TestCase):

    def test__is_published_recently__future_date__returns_false(self):
        future_date = timezone.now() + datetime.timedelta(days=30)
        question = Question.objects.create(date_published=future_date)

        self.assertFalse(question.is_published_recently())


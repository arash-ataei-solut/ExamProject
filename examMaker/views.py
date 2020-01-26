from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Exam
from .serializers import ExamSerializer


class ExamViewSet(ReadOnlyModelViewSet):
    serializer_class = ExamSerializer

    def get_queryset(self):
        exam_id = self.request.data.get('exam_id')
        return Exam.objects.get(id=exam_id)

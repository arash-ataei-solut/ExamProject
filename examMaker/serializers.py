from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField

from .models import Question, Exam


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ('text', 'A', 'B', 'C', 'D', 'question_level')


class ExamSerializer(ModelSerializer):
    exam_questions = SerializerMethodField()

    def get_exam_questions(self, exam):
        queryset = exam.questions.all()
        return QuestionSerializer(queryset, many=False, context={'exam':exam})

    class Meta:
        model = Exam
        fields = ('exam_questions', )

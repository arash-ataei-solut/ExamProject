from django.db import models
import random


class Category(models.Model):
    name = models.CharField(max_length=255)


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),

    ]
    answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    question_levels = [
        ('3', 'hard'),
        ('2', 'medium'),
        ('1', 'easy')
    ]
    question_level = models.CharField(max_length=1, choices=question_levels)


class ExamLevel(models.Model):
    level_name = models.CharField(max_length=255, unique=True)
    hard_questions = models.DecimalField(max_digits=2, decimal_places=0)
    medium_questions = models.DecimalField(max_digits=2, decimal_places=0)
    easy_questions = models.DecimalField(max_digits=2, decimal_places=0)
    time = models.DurationField()


class Exam(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(ExamLevel, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='MakeExam', through_fields=('exam', 'question'))

    def make(self):
        hard_questions = Question.objects.filter(category=self.category, question_level=3)
        medium_questions = Question.objects.filter(category=self.category, question_level=2)
        easy_questions = Question.objects.filter(category=self.category, question_level=1)
        questions = []
        questions += random.choices(hard_questions, weights=None, k=self.level.hard_questions)
        questions += random.choices(medium_questions, weights=None, k=self.level.medium_questions)
        questions += random.choices(easy_questions, weights=None, k=self.level.easy_questions)
        for q in questions:
            MakeExam(exam=self, question=q)


class MakeExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


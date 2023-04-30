from django.db import models
from django.contrib.auth.models import User
class Quizs(models.Model):
    title=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.title
class Questions(models.Model):
    quiz=models.ForeignKey(Quizs,on_delete=models.CASCADE)
    question=models.CharField(max_length=100)
    option1=models.CharField(max_length=50)
    option2=models.CharField(max_length=50)
    option3=models.CharField(max_length=50)
    option4=models.CharField(max_length=50)
    ans_choices=(("option1","Option 1"),("option2","Option 2"),("option3","Option 3"),("option4","Option 4"))
    answer=models.CharField(max_length=50,choices=ans_choices)
    def __str__(self) -> str:
        return self.question
    
class StudentResponse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    response = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.username} - {self.question.question}"

class ExamResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizs, on_delete=models.CASCADE)
    score = models.IntegerField()
    total=models.IntegerField(null=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
from datetime import date
class Video(models.Model):
    title=models.CharField(max_length=50)
    video_url=models.URLField()
    hidden_title=models.CharField(max_length=50)
    hidden_video_url=models.URLField()
    thumbnail=models.ImageField(upload_to='images/')
    quiz=models.ForeignKey(Quizs,on_delete=models.CASCADE ,null=True,blank=True)
    def __str__(self):
        return self.title
    
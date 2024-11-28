from django.db import models
from django_jalali.db import models as jmodels

class Question(models.Model):
    typeQuestion = [
    ('آسان','easy' ),
    ('متوسط','normal'),
    ('سخت' , 'hard' ),
    ]
    title = models.CharField(max_length = 20)
    Question_description = models.CharField(max_length = 3000000000000)
    date = jmodels.jDateField(auto_now_add=True)
    choice = models.CharField(max_length = 11 , choices=typeQuestion)
    
    def __str__(self) -> str:
        return f' title: {self.title}'
    
class User(models.Model):
    user = models.ForeignKey(Question , on_delete = models.CASCADE, null = True)
    answer = models.FileField(upload_to='my_images/', max_length=100 , null = True)
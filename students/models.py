from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    attendance = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.name
from django.db import models
from django.conf import settings

# Create your models here.

#Course Model
class Course(models.Model):
    code = models.CharField(max_length=20, unique= True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code

class TAProfile(models.Model):
    #one user, one TA profile
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE #delete a user, you delete the information associated with it
    )
    #one TA, multiple courses
    courses = models.ManyToManyField(
        Course,
        blank=True
    )

    def __str__(self):
        return self.user.username

#TA availability, start times, end times. 
# ta= tutoring hours. ForeignKey= OneToMany relationship
class TutoringHour(models.Model):
    ta = models.ForeignKey(
        TAProfile, 
        on_delete=models.CASCADE,   
        related_name="tutoring_hours"
    )
    day =models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.ta} - {self.day}"
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    usn = models.CharField(max_length=11, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()

class Marks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.FloatField()
    grade = models.CharField(max_length=2, blank=True, null=True)
    grade_points = models.IntegerField(blank=True, null=True)
    credit_points = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'semester', 'course')

    def save(self, *args, **kwargs):
        self.grade, self.grade_points = self.calculate_grade(self.marks)
        self.credit_points = self.grade_points * self.course.credits
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_grade(marks):
        if marks > 89:
            return 'O', 10
        elif marks > 79:
            return 'A+', 9
        elif marks > 69:
            return 'A', 8
        elif marks > 59:
            return 'B+', 7
        elif marks > 54:
            return 'B', 6
        elif marks > 49:
            return 'C', 5
        elif marks > 39:
            return 'P', 4
        else:
            return 'F', 0

class NonCreditCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=2)

class PerformanceAnalytics(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.IntegerField()
    sgpa = models.FloatField()
    cgpa = models.FloatField()

class MentorAssignment(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_mentor')
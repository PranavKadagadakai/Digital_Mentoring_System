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

class PerformanceAnalytics(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.IntegerField()
    sgpa = models.FloatField()
    cgpa = models.FloatField()
    
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

        # Update Performance Analytics
        self.update_performance_analytics()

    def update_performance_analytics(self):
        """ Update SGPA for the current semester and CGPA overall. """
        student = self.student
        semester = self.semester

        # Fetch all marks for the student in the semester
        marks_entries = Marks.objects.filter(student=student, semester=semester)
        total_credits = sum(entry.course.credits for entry in marks_entries)
        total_credit_points = sum(entry.credit_points for entry in marks_entries)

        # Compute SGPA
        sgpa = round(total_credit_points / total_credits, 2) if total_credits else 0.0

        # Compute CGPA
        all_marks = Marks.objects.filter(student=student)
        all_total_credits = sum(entry.course.credits for entry in all_marks)
        all_total_credit_points = sum(entry.credit_points for entry in all_marks)
        cgpa = round(all_total_credit_points / all_total_credits) if all_total_credits > 0 else 0

        # Update PerformanceAnalytics Table
        PerformanceAnalytics.objects.update_or_create(
            student=student, semester=semester,
            defaults={'sgpa': round(sgpa, 2), 'cgpa': round(cgpa, 2)}
        )

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

class MentorAssignment(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_mentor')
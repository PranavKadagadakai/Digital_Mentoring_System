from .models import Marks

def calculate_sgpa(student, semester):
    marks = Marks.objects.filter(student=student, semester=semester)
    total_credit_points = sum(m.credit_points for m in marks)
    total_credits = sum(m.course.credits for m in marks)
    return round(total_credit_points / total_credits, 2) if total_credits else 0.0

def calculate_cgpa(student):
    marks = Marks.objects.filter(student=student)
    total_credit_points = sum(m.credit_points for m in marks if m.grade != 'F')
    total_credits = sum(m.course.credits for m in marks if m.grade != 'F')
    return round(total_credit_points / total_credits, 2) if total_credits else 0.0
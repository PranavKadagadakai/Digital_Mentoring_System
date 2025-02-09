from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Marks, Course, NonCreditCourse, User, PerformanceAnalytics, MentorAssignment
from .utils import calculate_sgpa, calculate_cgpa
import logging
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def custom_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password."
    return render(request, 'core/login.html', {'error_message': error_message})

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing_page.html')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'core/profile.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    context = {
        'name': user.full_name,
        'usn': user.usn,
        'phone_number': user.phone_number,
        'profile_photo': user.profile_photo.url if user.profile_photo else None,
        'role': user.role,
    }

    if user.role == 'student':
        context['scoreboard'] = Marks.objects.filter(student=user)
        context['grade_card'] = PerformanceAnalytics.objects.filter(student=user)
        context['semesters'] = sorted(set(Marks.objects.filter(student=user).values_list('semester', flat=True)))
    elif user.role == 'mentor':
        assigned_students = MentorAssignment.objects.filter(mentor=user).values_list('student', flat=True)
        students = User.objects.filter(id__in=assigned_students)
        context['students'] = students
        context['semesters'] = sorted(set(Marks.objects.filter(student__in=students).values_list('semester', flat=True)))
        context['can_input_marks'] = True
    elif user.role == 'admin':
        context['students'] = User.objects.filter(role='student')
        context['mentors'] = User.objects.filter(role='mentor')
        context['assignments'] = MentorAssignment.objects.all()

    return render(request, 'core/dashboard.html', context)

@login_required
def scoreboard(request):
    student = request.user
    semesters = set(Marks.objects.filter(student=student).values_list('semester', flat=True))
    semester_data = []
    for semester in semesters:
        sgpa = calculate_sgpa(student, semester)
        courses = Marks.objects.filter(student=student, semester=semester)
        semester_data.append({'semester': semester, 'sgpa': sgpa, 'courses': courses})
    cgpa = calculate_cgpa(student)
    return render(request, 'core/scoreboard.html', {'semester_data': semester_data, 'cgpa': cgpa})

@login_required
def input_marks(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        semester = request.POST.get('semester')
        courses_data = zip(
            request.POST.getlist('course_code'),
            request.POST.getlist('course_name'),
            map(int, request.POST.getlist('credits')),
            map(float, request.POST.getlist('marks'))
        )

        student = get_object_or_404(User, id=student_id)
        
        for course_code, course_name, credits, marks in courses_data:
            course, created = Course.objects.get_or_create(
                course_code=course_code,
                defaults={'course_name': course_name, 'credits': credits}
            )
            try:
                Marks.objects.update_or_create(
                    student=student,
                    semester=semester,
                    course=course,
                    defaults={'marks': marks}
                )
            except IntegrityError:
                continue  # Handle duplicate course entries gracefully

        return redirect('grade_card', student_id=student.id, semester=semester)

    students = User.objects.filter(role='student')
    return render(request, 'core/input_marks.html', {'students': students})

@login_required
def assign_mentor(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor')
        student_id = request.POST.get('student')
        mentor = get_object_or_404(User, id=mentor_id, role='mentor')
        student = get_object_or_404(User, id=student_id, role='student')
        MentorAssignment.objects.create(mentor=mentor, student=student)
        return redirect('dashboard')
    return render(request, 'core/assign_mentor.html', {'mentors': User.objects.filter(role='mentor'), 'students': User.objects.filter(role='student')})

@login_required
def grade_card(request, student_id = None, semester=None):
    student = get_object_or_404(User, id=student_id)
    semesters = sorted(set(Marks.objects.filter(student=student).values_list('semester', flat=True)))
    selected_semester = request.GET.get('semester', semesters[0] if semesters else None)
    marks = Marks.objects.filter(student=student, semester=selected_semester)
    non_credit_courses = NonCreditCourse.objects.filter(student=student)
    total_credits = sum(mark.course.credits for mark in marks)
    total_credit_points = sum(mark.credit_points for mark in marks)
    sgpa = total_credit_points / total_credits if total_credits > 0 else 0
    cgpa = calculate_cgpa(student=student)
    return render(request, 'core/grade_card.html', {
        'student': student,
        'semesters': semesters,
        'selected_semester': int(selected_semester) if selected_semester else None,
        'marks': marks,
        'non_credit_courses': non_credit_courses,
        'sgpa': round(sgpa, 2),
        'cgpa': round(cgpa, 2)
    })

@login_required
def result_analysis(request):
    user = request.user
    try:
        if user.role == 'student':
            performance_data = PerformanceAnalytics.objects.filter(student=user).order_by('semester')

            if not performance_data.exists():
                logger.warning(f"No performance data found for user: {user.username}")
                return JsonResponse({'error': 'No performance data found'}, status=404)

            data = {
                'semesters': [p.semester for p in performance_data],
                'sgpa': [p.sgpa for p in performance_data]
            }
            logger.info(f"Sending data: {data}")
            return JsonResponse(data, content_type="application/json", safe=False)

        elif user.role == 'mentor':
            assigned_students = MentorAssignment.objects.filter(mentor=user).values_list('student', flat=True)
            students = User.objects.filter(id__in=assigned_students)

            student_data = {}
            for student in students:
                performance = PerformanceAnalytics.objects.filter(student=student).order_by('semester')
                
                if performance.exists():
                    student_data[student.full_name] = {
                        'semesters': [p.semester for p in performance],
                        'sgpa': [p.sgpa for p in performance]
                    }
                else:
                    logger.warning(f"No performance data for student: {student.full_name}")

            if not student_data:
                return JsonResponse({'error': 'No student performance data available'}, status=404)

            logger.info(f"Sending data: {student_data}")
            return JsonResponse({'students': student_data}, content_type="application/json", safe=False)

        else:
            logger.error(f"Unauthorized access attempt by {user.username}")
            return JsonResponse({'error': 'Unauthorized'}, status=403)

    except Exception as e:
        logger.exception(f"Error in result_analysis view: {str(e)}")
        return JsonResponse({'error': 'An error occurred while fetching data'}, status=500)

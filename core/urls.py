from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('input-marks/', views.input_marks, name='input_marks'),
    path('grade-card/<int:student_id>/', views.grade_card, name='grade_card'),
    path('result-analysis/', views.result_analysis, name='result_analysis'),
    # path('export-csv/', views.export_csv, name='export_csv'),
    path('assign-mentor/', views.assign_mentor, name='assign_mentor'),
    path('profile/', views.profile, name='profile'),
]
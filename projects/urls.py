from django.urls import path
from projects import views

app_name = 'projects'
urlpatterns = [
    path('', views.home, name='home'),
    # project-specific urls
    path('all/', views.view_all_projects, name='view_all_projects'),
    path('create-project/', views.create_project, name='create_project'),
    path('projects/<str:project_slug>/', views.view_project, name='view_project'),
    path('projects/<str:project_slug>/enroll/', views.enroll, name='enroll'),
    path('projects/<str:project_slug>/update', views.update_project, name='update'),

    # solution-specific urls
    path('create-solution/<str:project_slug>/', views.create_solution, name='create_solution'),
    path('solutions/', views.view_all_solutions, name='view_all_solutions'),
    path('solutions/<str:uid>/', views.view_solution, name='view_solution'),
    path('solutions/<str:uid>/update/', views.update_solution, name='update_solution'),
]
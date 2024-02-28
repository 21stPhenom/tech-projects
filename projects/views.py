from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.models import Profile
from projects.models import Project, Solution

# Create your views here.
class Home(View):
    model = Project
    template_name = 'projects/home.html'

    def get(self, request, *args, **kwargs):
        projects = self.model.objects.all()[0:3]
        solutions = Solution.objects.all()[0:3]
        context = {
            'projects': projects,
            'solutions': solutions
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class CreateProject(View):
    model = Project
    template_name = 'projects/create_project.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile

        name = request.POST['project_name']
        short_description = request.POST['short_description']
        long_description = request.POST['long_description']
        tags = request.POST['tags']
        difficulty = int(request.POST['project_difficulty'])


        if self.model.objects.filter(name=name).exists():
            messages.error(request, 'A project with the same name already exists.')
            print('Project with same name already exists.')

        new_project = self.model.objects.create(
            creator=profile,
            name=name,
            short_description=short_description,
            long_description=long_description,
            difficulty=difficulty,
            tags=tags
        )
        print('Project created.')
        # return redirect('accounts:my_projects')
        return redirect('projects:view_project', new_project.project_slug)
    
class ViewProject(View):
    model = Project
    template_name = 'projects/view_project.html'

    def get(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)

        # check if a user is logged and has enrolled in a project
        if request.user.is_authenticated and \
        project.enrolled_profiles.contains(request.user.profile):
            enrolled = True
        else:
            enrolled = False

        solutions = Solution.objects.filter(project=project)
        context = {
            'project': project,
            'solutions': solutions,
            'enrolled': enrolled
        }
        return render(request, self.template_name, context)

class ViewAllProjects(View):
    model = Project
    template_name = "projects/all_projects.html"

    def get(self, request, *args, **kwargs):
        projects = self.model.objects.all()
        context = {
            'projects': projects
        }
        return render(request, self.template_name, context)
        
@method_decorator(login_required, name='dispatch')
class Enroll(View):
    model = Project

    def get(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        profile = get_object_or_404(Profile, user=request.user)
        
        project.enrolled_profiles.add(profile)
        messages.success(request, 'You have successfully enrolled in this project.')

        return redirect('projects:view_project', project_slug)

@method_decorator(login_required, name='dispatch')
class UpdateProject(View):
    model = Project
    template_name = 'projects/update_project.html'

    def get(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        profile = request.user.profile

        if profile != project.creator:
            print('can not update project')
            raise PermissionDenied(f'{profile} cannot edit this project.')
        
        context = {
            'project': project
        }
        return render(request, self.template_name, context)
    
    def post(self, request, project_slug, *args, **kwargs):
        project = get_object_or_404(self.model, project_slug=project_slug)
        profile = request.user.profile

        if profile != project.creator:
            print('can not update project')
            raise PermissionDenied(f'{profile} cannot edit this project.')
        
        project.name = request.POST['project_name']
        project.short_description = request.POST['short_description']
        project.long_description = request.POST['long_description']
        project.difficulty = int(request.POST['project_difficulty'])
        tags = request.POST['tags']
        if type(tags) == str:
            project.tags.append(tags)
        elif type(tags) == list:
            project.tags.extend(tags)
        else:
            pass

        project.save(update_fields=['name', 'short_description', 'long_description', 'difficulty', 'tags'])
        
        print('project updated.')

        return redirect('projects:view_project')

@method_decorator(login_required, name='dispatch')
class CreateSolution(View):
    model = Solution

    def post(self, request, project_slug, *args, **kwargs):
        creator = request.user.profile
        project = get_object_or_404(Project, project_slug=project_slug)
        name = request.POST['name']
        repo_link = request.POST['repo_link']
        live_link = request.POST.get('live_link', None)

        if not project.enrolled_profiles.contains(creator):
            messages.error(request, "You must enroll before you can submit a solution")
            print("Enroll to submit solution.")

        if live_link == None:
            new_solution = self.model.objects.create(
                creator=creator,
                name=name,
                project=project,
                repo_link=repo_link
            )
            print(f'New solution for project {project.name}')
        elif live_link != None:
            new_solution = self.model.objects.create(
                creator=creator,
                name=name,
                project=project,
                repo_link=repo_link,
                live_link=live_link
            )
            print(f'New solution for project {project.name}')
        return redirect("projects:view_project", project_slug)
        
class ViewSolution(View):
    model = Solution
    template_name = 'projects/view_solution.html'

    def get(self, request, uid, *args, **kwargs):
        solution = get_object_or_404(self.model, uid=uid)
        context = {
            'solution': solution
        }
        return render(request, self.template_name, context)

class ViewAllSolutions(View):
    model = Solution
    template_name = 'projects/view_solutions.html'

    def get(self, request, *args, **kwargs):
        solutions = self.model.objects.all()
        context = {
            'solutions': solutions
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class UpdateSolution(View):
    model = Solution
    template_name = 'projects/update_solution.html'

    def get(self, request, uid, *args, **kwargs):
        solution = get_object_or_404(self.model, id=uid)
        user_profile = request.user.profile

        if solution.creator != user_profile:
            print('can not update solution')
            raise PermissionDenied(f'{user_profile} cannot edit this project.')

        context = {
            'solution': solution
        }
        
        return render(request, self.template_name, context)

    def post(self, request, uid, *args, **kwargs):
        solution = get_object_or_404(self.model, uid=uid)
        user_profile = request.user.profile

        if solution.creator != user_profile:
            print('can not update solution')
            raise PermissionDenied(f'{user_profile} cannot edit this project.')

        name = request.POST.get('name', None)
        solution.repo_link = request.POST['repo_link']
        live_link = request.POST.get('live_link', None)
        
        if name != None and type(name) == str:
            solution.name = name            
            
        if live_link == None:
            solution.save(update_fields=['name', 'repo_link'])
        elif live_link != None:
            solution.live_link = live_link
            solution.save(update_fields=['name', 'repo_link', 'live_link'])

        print('Solution updated.')
        return redirect('projects:view_solutions')

# project-specific views
home = Home.as_view()
create_project = CreateProject.as_view()
view_project = ViewProject.as_view()
view_all_projects = ViewAllProjects.as_view()
enroll = Enroll.as_view()
update_project = UpdateProject.as_view()

# solution-specific views
create_solution = CreateSolution.as_view()
view_solution = ViewSolution.as_view()
view_all_solutions = ViewAllSolutions.as_view()
update_solution = UpdateSolution.as_view()
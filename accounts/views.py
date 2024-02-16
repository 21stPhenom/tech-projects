from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import Profile

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/home.html')
    
class Register(View):
    def get(self, request, *args, **kwargs):
        request.session['next'] = request.META.get('HTTP_REFERER', None)
        return render(request, 'accounts/register.html')

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']


        if User.objects.filter(email=email).exists():
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            return redirect('accounts:register')

        if password_1 != password_2:
            return redirect('accounts:register')
        
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password_1
        )

        try:
            profile = Profile.objects.get(user=new_user)
        except Profile.DoesNotExist:
            profile  = Profile.objects.create(user=new_user)    
        
        if request.session['next']:
            return redirect(request.session['next'])
        
        return redirect('accounts:login')

class Login(View):
    
    def get(self, request, *args, **kwargs):
        if 'next' in request.GET:
            request.session['next'] = request.GET['next']
        else:
            request.session['next'] = request.META.get('HTTP_REFERER')
        return render(request, 'accounts/login.html')
        
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('Logged In')
        else:
            print('Invalid credentials')
            return redirect('accounts:login')
        
        if request.session['next']:
            return redirect(request.session['next'])
        else:
            return redirect('accounts:home')

@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(Self, request, *args, **kwargs):
        request.session['next'] = request.META.get('HTTP_REFERER')
        logout(request)

        if request.session.get('next', None):
            return redirect(request.session['next'])
        else:
            return redirect('accounts:home')

home_view = Home.as_view()
register_view = Register.as_view()
login_view = Login.as_view()
logout_view = Logout.as_view()
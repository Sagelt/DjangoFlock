# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render_to_response('base.html')

def register_view(request):
    return render_to_response('signup.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
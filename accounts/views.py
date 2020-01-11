from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm

# Create your views here.
def signup_views(req):
    if req.method == 'POST': 
        form = SignUpForm(req.POST) 
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(req, 'signup.html', {'form':form})

from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from accounts.forms import SignUpForm


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


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
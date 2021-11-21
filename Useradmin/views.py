from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import MySignUpForm
from .models import MyUser
from Useradmin.models import get_myuser_from_user


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'],
                                        email=data['email'],
                                        )
        my_user = MyUser.objects.create(user=user,
                                        date_of_birth=data['date_of_birth'],
                                        profile_picture=data['profile_picture'],
                                        )
        return redirect('login')


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in. PERFORM CUSTOM CODE."""
        auth_login(self.request, form.get_user())

        # execute_after_login() is in MyUser class
        # If there is a MyUser object behind the User object,
        # access it and call execute_after_login()
        user = form.get_user()  # Class is User, not MyUser
        #print('-------------', user.__class__.__name__)
        myuser = get_myuser_from_user(user)
        if myuser is not None:
            myuser.execute_after_login()  # Custom code
        return HttpResponseRedirect(self.get_success_url())


class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser-list.html'


class HomeBirthdayView(TemplateView):
    def get_context_data(self, **kwargs):
        user = self.request.user  # Class is User, not MyUser
        #print('-------------', user.__class__.__name__)
        myuser_has_birthday_today = False
        if user.is_authenticated:  # Anonymous user cannot call has_birthday_today()

            # It is possible to have a User object without a
            # corresponding MyUser object, e.g. superuser
            myuser = get_myuser_from_user(user)
            if myuser is not None:
                myuser_has_birthday_today = myuser.has_birthday_today()

        context = super(HomeBirthdayView, self).get_context_data(**kwargs)
        context['myuser_has_birthday_today'] = myuser_has_birthday_today
        return context

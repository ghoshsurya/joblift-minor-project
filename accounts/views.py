from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

def admin_users_list(request):
    if not request.user.is_staff:
        return redirect('/admin/')
    
    users = CustomUser.objects.all()
    html = """
    <h1>All Users</h1>
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <tr>
            <th>ID</th><th>Username</th><th>Email</th><th>First Name</th><th>Last Name</th>
            <th>Phone</th><th>Job Role</th><th>Experience</th><th>Active</th><th>Staff</th>
        </tr>
    """
    
    for user in users:
        html += f"""
        <tr>
            <td>{user.id}</td>
            <td><a href="/admin/accounts/customuser/{user.id}/change/">{user.username}</a></td>
            <td>{user.email}</td>
            <td>{user.first_name}</td>
            <td>{user.last_name}</td>
            <td>{user.phone or ''}</td>
            <td>{user.preferred_job_role or ''}</td>
            <td>{user.experience_level}</td>
            <td>{'Yes' if user.is_active else 'No'}</td>
            <td>{'Yes' if user.is_staff else 'No'}</td>
        </tr>
        """
    
    html += "</table>"
    return HttpResponse(html)

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, f'Welcome {user.username}! Your account has been created.')
        return response

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

class LogoutView(BaseLogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
from django.contrib import admin
from django.db import models
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'preferred_job_role', 'experience_level', 'is_active')
    list_filter = ('experience_level', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Handle search
        query = request.GET.get('q', '')
        if query:
            users = CustomUser.objects.filter(
                models.Q(username__icontains=query) |
                models.Q(email__icontains=query) |
                models.Q(first_name__icontains=query) |
                models.Q(last_name__icontains=query) |
                models.Q(phone__icontains=query) |
                models.Q(preferred_job_role__icontains=query)
            )
        else:
            users = CustomUser.objects.all()
            
        extra_context['object_list'] = users
        extra_context['search_query'] = query
        return super().changelist_view(request, extra_context)
from django.contrib import admin
from .models import JobPortal, JobListing, UserJobAlert

@admin.register(JobPortal)
class JobPortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'base_url')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['object_list'] = JobPortal.objects.all()
        return super().changelist_view(request, extra_context)

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'portal', 'posted_date', 'is_recent')
    list_filter = ('portal', 'job_type', 'is_recent', 'posted_date')
    search_fields = ('title', 'company', 'location', 'description')
    readonly_fields = ('scraped_at',)
    ordering = ('-posted_date',)
    
    actions = ['mark_as_recent', 'mark_as_old']
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['object_list'] = JobListing.objects.all().order_by('-posted_date')
        return super().changelist_view(request, extra_context)
    
    def mark_as_recent(self, request, queryset):
        queryset.update(is_recent=True)
    mark_as_recent.short_description = "Mark selected jobs as recent"
    
    def mark_as_old(self, request, queryset):
        queryset.update(is_recent=False)
    mark_as_old.short_description = "Mark selected jobs as old"

@admin.register(UserJobAlert)
class UserJobAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'keywords', 'location', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('user__username', 'keywords', 'location')
    ordering = ('-created_at',)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['object_list'] = UserJobAlert.objects.all().order_by('-created_at')
        return super().changelist_view(request, extra_context)
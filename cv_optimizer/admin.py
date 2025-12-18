from django.contrib import admin
from .models import CVUpload, ATSKeyword, CVTemplate, CreatedCV

@admin.register(CVUpload)
class CVUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_role', 'ats_score', 'created_at')
    list_filter = ('job_role', 'created_at', 'ats_score')
    search_fields = ('user__username', 'user__email', 'job_role')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['object_list'] = CVUpload.objects.all().order_by('-created_at')
        return super().changelist_view(request, extra_context)

@admin.register(ATSKeyword)
class ATSKeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'category', 'weight')
    list_filter = ('category',)
    search_fields = ('keyword', 'category')
    ordering = ('category', 'keyword')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['object_list'] = ATSKeyword.objects.all().order_by('category', 'keyword')
        return super().changelist_view(request, extra_context)

@admin.register(CVTemplate)
class CVTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'description']

@admin.register(CreatedCV)
class CreatedCVAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'template', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['full_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
from django.urls import path
from . import views, latex_compiler_new, ai_views

app_name = 'cv_optimizer'

urlpatterns = [
    path('upload/', views.CVUploadView.as_view(), name='upload'),
    path('analyze/<slug:job_role>/<int:cv_id>/', views.CVAnalysisView.as_view(), name='analyze'),
    path('optimize/<int:cv_id>/', views.CVOptimizeView.as_view(), name='optimize'),
    path('download/<int:cv_id>/', views.DownloadOptimizedCV.as_view(), name='download'),
    path('delete/<int:cv_id>/', views.DeleteCVView.as_view(), name='delete'),
    path('delete-multiple/', views.DeleteMultipleCVView.as_view(), name='delete_multiple'),
    path('history/', views.CVHistoryView.as_view(), name='history'),
    
    # AI-Powered Features
    path('ai-optimized/<int:cv_id>/', ai_views.AIOptimizedCVView.as_view(), name='ai_optimized'),
    path('ai-download/<int:cv_id>/', ai_views.DownloadOptimizedAICVView.as_view(), name='ai_download'),
    path('job-matching/<int:cv_id>/', ai_views.JobMatchingView.as_view(), name='job_matching'),
    path('application-guide/', ai_views.JobApplicationGuideView.as_view(), name='application_guide'),
    path('regenerate-analysis/<int:cv_id>/', ai_views.RegenerateAnalysisView.as_view(), name='regenerate_analysis'),
    path('custom-job-search/', ai_views.CustomJobSearchView.as_view(), name='custom_job_search'),
    
    # CV Creation URLs
    path('create/', views.CVCreateView.as_view(), name='create'),
    path('create/templates/', views.CVTemplateListView.as_view(), name='templates'),
    path('create/<int:template_id>/', views.CVBuilderView.as_view(), name='builder'),
    path('created/', views.CreatedCVListView.as_view(), name='created_list'),
    path('created/<int:cv_id>/', views.CreatedCVDetailView.as_view(), name='created_detail'),
    path('created/<int:cv_id>/download/', views.DownloadCreatedCVView.as_view(), name='download_created'),
    path('created/<int:cv_id>/edit/', views.EditCreatedCVView.as_view(), name='edit_created'),
    path('created/<int:cv_id>/delete/', views.DeleteCreatedCVView.as_view(), name='delete_created'),
    path('template/<int:template_id>/preview/', views.TemplatePreviewView.as_view(), name='template_preview'),
    path('latex-editor/', views.LaTeXEditorView.as_view(), name='latex_editor'),
    path('latex/compile/', latex_compiler_new.CompileLaTeXView.as_view(), name='compile_latex'),
]
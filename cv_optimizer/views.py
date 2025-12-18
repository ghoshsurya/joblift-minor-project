from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, DeleteView, TemplateView, View
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from .models import CVUpload, CreatedCV, CVTemplate
from .forms import CVUploadForm, CVCreationForm
from .utils import analyze_cv, optimize_cv, generate_cv_pdf, extract_text_from_file
from .gemini_service import GeminiCVAnalyzer
from .job_matcher import JobMatcher
import json

class CVUploadView(LoginRequiredMixin, CreateView):
    model = CVUpload
    form_class = CVUploadForm
    template_name = 'cv_optimizer/upload.html'
    success_url = reverse_lazy('cv_optimizer:history')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Perform Gemini AI analysis
        try:
            cv_text = extract_text_from_file(self.object.original_cv.path)
            gemini_analyzer = GeminiCVAnalyzer()
            analysis = gemini_analyzer.analyze_cv(cv_text, form.instance.job_role)
            
            # Save analysis results
            self.object.gemini_analysis = analysis
            self.object.ats_score = analysis.get('ats_score', 0)
            self.object.missing_sections = analysis.get('missing_sections', [])
            self.object.improvement_suggestions = analysis.get('improvements', [])
            self.object.keyword_suggestions = analysis.get('keyword_suggestions', [])
            self.object.job_match_percentage = analysis.get('job_match_percentage', 0)
            
            # Generate optimized CV content
            optimized_content = gemini_analyzer.generate_optimized_cv(cv_text, analysis)
            self.object.optimized_content = optimized_content
            
            self.object.save()
            
            messages.success(self.request, 'CV uploaded and analyzed successfully!')
        except Exception as e:
            messages.warning(self.request, f'CV uploaded but analysis failed: {str(e)}')
        
        return response

class CVAnalysisView(LoginRequiredMixin, DetailView):
    model = CVUpload
    template_name = 'cv_optimizer/analysis.html'
    context_object_name = 'cv_upload'
    
    def get_object(self):
        job_role_slug = self.kwargs.get('job_role')
        unique_id = int(self.kwargs.get('cv_id'))
        
        # Convert slug back to job role
        job_role = job_role_slug.replace('-', ' ').title()
        
        # Get user's CVs for this job role ordered by creation date
        user_cvs = CVUpload.objects.filter(
            user=self.request.user,
            job_role__icontains=job_role_slug.replace('-', ' ')
        ).order_by('created_at')
        
        # Get the CV at the specified index
        try:
            cv = user_cvs[unique_id - 1]
            if cv:
                return cv
        except (IndexError, TypeError):
            pass
        
        # Fallback: return any CV from user
        return CVUpload.objects.filter(user=self.request.user).first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cv_upload = self.get_object()
        
        # Perform analysis
        analysis = analyze_cv(cv_upload.original_cv.path, cv_upload.job_role)
        cv_upload.ats_score = analysis['score']
        cv_upload.save()
        
        context['analysis'] = analysis
        return context

class CVOptimizeView(LoginRequiredMixin, DetailView):
    model = CVUpload
    template_name = 'cv_optimizer/optimize.html'
    context_object_name = 'cv_upload'
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        cv_upload = self.get_object()
        
        if not cv_upload.optimized_cv:
            # Generate optimization tips
            analysis = analyze_cv(cv_upload.original_cv.path, cv_upload.job_role)
            optimization_tips = optimize_cv(cv_upload.original_cv.path, analysis)
            messages.info(request, 'Optimization tips generated based on current analysis.')
        
        messages.success(request, 'CV optimization tips generated successfully!')
        return redirect('cv_optimizer:analyze', job_role=cv_upload.get_job_role_slug(), cv_id=cv_upload.get_unique_id())

class DownloadOptimizedCV(LoginRequiredMixin, DetailView):
    model = CVUpload
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        cv_upload = self.get_object()
        
        if cv_upload.optimized_cv:
            response = HttpResponse(cv_upload.optimized_cv.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="optimized_{cv_upload.original_cv.name}"'
            return response
        
        messages.error(request, 'Optimized CV not available.')
        return redirect('cv_optimizer:analyze', job_role=cv_upload.get_job_role_slug(), cv_id=cv_upload.get_unique_id())

class CVHistoryView(LoginRequiredMixin, ListView):
    model = CVUpload
    template_name = 'cv_optimizer/history.html'
    context_object_name = 'cv_uploads'
    paginate_by = 10
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)

class DeleteCVView(LoginRequiredMixin, DeleteView):
    model = CVUpload
    pk_url_kwarg = 'cv_id'
    success_url = reverse_lazy('cv_optimizer:history')
    
    def get_queryset(self):
        return CVUpload.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'CV analysis deleted successfully!')
        return super().delete(request, *args, **kwargs)

class DeleteMultipleCVView(LoginRequiredMixin, View):
    def post(self, request):
        cv_ids = request.POST.getlist('cv_ids')
        if cv_ids:
            deleted_count = CVUpload.objects.filter(
                id__in=cv_ids, 
                user=request.user
            ).delete()[0]
            messages.success(request, f'{deleted_count} CV analyses deleted successfully!')
        return redirect('cv_optimizer:history')

# CV Creation Views
class CVCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'cv_optimizer/create_options.html'

class CVTemplateListView(LoginRequiredMixin, ListView):
    model = CVTemplate
    template_name = 'cv_optimizer/template_list.html'
    context_object_name = 'templates'
    
    def get_queryset(self):
        return CVTemplate.objects.filter(is_active=True)

class CVBuilderView(LoginRequiredMixin, CreateView):
    model = CreatedCV
    form_class = CVCreationForm
    template_name = 'cv_optimizer/cv_builder.html'
    
    def form_invalid(self, form):
        print(f"Form is invalid. Errors: {form.errors}")
        print(f"POST data: {self.request.POST}")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = get_object_or_404(CVTemplate, id=self.kwargs['template_id'])
        return context
    
    def form_valid(self, form):
        print(f"Form is valid. POST data: {self.request.POST}")
        form.instance.user = self.request.user
        form.instance.template = get_object_or_404(CVTemplate, id=self.kwargs['template_id'])
        print(f"Template found: {form.instance.template.name}")
        
        # Process dynamic form data
        experience = []
        education = []
        skills = {}
        
        # Extract experience data
        i = 0
        while f'exp_title_{i}' in self.request.POST:
            if self.request.POST.get(f'exp_title_{i}'):
                experience.append({
                    'title': self.request.POST.get(f'exp_title_{i}'),
                    'company': self.request.POST.get(f'exp_company_{i}'),
                    'start_date': self.request.POST.get(f'exp_start_{i}'),
                    'end_date': self.request.POST.get(f'exp_end_{i}'),
                    'description': self.request.POST.get(f'exp_desc_{i}')
                })
            i += 1
        
        # Extract education data
        i = 0
        while f'edu_degree_{i}' in self.request.POST:
            if self.request.POST.get(f'edu_degree_{i}'):
                education.append({
                    'degree': self.request.POST.get(f'edu_degree_{i}'),
                    'institution': self.request.POST.get(f'edu_institution_{i}'),
                    'year': self.request.POST.get(f'edu_year_{i}'),
                    'grade': self.request.POST.get(f'edu_grade_{i}')
                })
            i += 1
        
        # Extract skills data
        i = 0
        while f'skill_category_{i}' in self.request.POST:
            category = self.request.POST.get(f'skill_category_{i}')
            skill_list = self.request.POST.get(f'skill_list_{i}')
            if category and skill_list:
                skills[category] = [skill.strip() for skill in skill_list.split(',')]
            i += 1
        
        form.instance.experience = experience
        form.instance.education = education
        form.instance.skills = skills
        
        try:
            result = super().form_valid(form)
            print(f"CV created successfully with ID: {self.object.id}")
            return result
        except Exception as e:
            print(f"Error creating CV: {e}")
            raise
    
    def get_success_url(self):
        return reverse_lazy('cv_optimizer:created_detail', kwargs={'cv_id': self.object.id})

class CreatedCVListView(LoginRequiredMixin, ListView):
    model = CreatedCV
    template_name = 'cv_optimizer/created_list.html'
    context_object_name = 'created_cvs'
    
    def get_queryset(self):
        return CreatedCV.objects.filter(user=self.request.user)

class CreatedCVDetailView(LoginRequiredMixin, DetailView):
    model = CreatedCV
    template_name = 'cv_optimizer/created_detail.html'
    context_object_name = 'cv'
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CreatedCV.objects.filter(user=self.request.user)

class DownloadCreatedCVView(LoginRequiredMixin, DetailView):
    model = CreatedCV
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CreatedCV.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        cv = self.get_object()
        
        # Generate PDF if not exists
        if not cv.pdf_file:
            pdf_path = generate_cv_pdf(cv)
            cv.pdf_file = pdf_path
            cv.save()
        
        response = HttpResponse(cv.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv.full_name}_CV.pdf"'
        return response

class EditCreatedCVView(LoginRequiredMixin, DetailView):
    model = CreatedCV
    template_name = 'cv_optimizer/edit_cv.html'
    context_object_name = 'cv'
    pk_url_kwarg = 'cv_id'
    
    def get_queryset(self):
        return CreatedCV.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        cv = self.get_object()
        
        # Update CV fields
        cv.full_name = request.POST.get('full_name', cv.full_name)
        cv.email = request.POST.get('email', cv.email)
        cv.phone = request.POST.get('phone', cv.phone)
        cv.address = request.POST.get('address', cv.address)
        cv.linkedin_url = request.POST.get('linkedin_url', cv.linkedin_url)
        cv.portfolio_url = request.POST.get('portfolio_url', cv.portfolio_url)
        cv.professional_summary = request.POST.get('professional_summary', cv.professional_summary)
        
        cv.save()
        messages.success(request, 'CV updated successfully!')
        return redirect('cv_optimizer:created_detail', cv_id=cv.id)

class DeleteCreatedCVView(LoginRequiredMixin, DeleteView):
    model = CreatedCV
    pk_url_kwarg = 'cv_id'
    success_url = reverse_lazy('cv_optimizer:created_list')
    
    def get_queryset(self):
        return CreatedCV.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'CV deleted successfully!')
        return super().delete(request, *args, **kwargs)

class TemplatePreviewView(DetailView):
    model = CVTemplate
    template_name = 'cv_optimizer/template_preview.html'
    context_object_name = 'template'
    pk_url_kwarg = 'template_id'

class LaTeXEditorView(LoginRequiredMixin, TemplateView):
    template_name = 'cv_optimizer/latex_editor.html'

class CompileLaTeXView(LoginRequiredMixin, View):
    def post(self, request):
        import subprocess
        import tempfile
        import os
        
        try:
            data = json.loads(request.body)
            latex_code = data.get('latex', '')
            
            # Create temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tex_file:
                tex_file.write(latex_code)
                tex_path = tex_file.name
            
            # Compile LaTeX to PDF
            output_dir = os.path.dirname(tex_path)
            result = subprocess.run(
                ['pdflatex', '-output-directory', output_dir, tex_path],
                capture_output=True, text=True
            )
            
            pdf_path = tex_path.replace('.tex', '.pdf')
            
            if os.path.exists(pdf_path):
                # Move PDF to media directory
                import shutil
                from django.conf import settings
                
                media_path = os.path.join(settings.MEDIA_ROOT, 'latex_pdfs')
                os.makedirs(media_path, exist_ok=True)
                
                final_pdf = os.path.join(media_path, f'cv_{request.user.id}.pdf')
                shutil.move(pdf_path, final_pdf)
                
                pdf_url = f'/media/latex_pdfs/cv_{request.user.id}.pdf'
                
                # Cleanup
                os.unlink(tex_path)
                
                return JsonResponse({'success': True, 'pdf_url': pdf_url})
            else:
                return JsonResponse({'success': False, 'error': result.stderr})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
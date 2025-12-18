from django import forms
from .models import CVUpload, CreatedCV, CVTemplate

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CVUpload
        fields = ['job_role', 'original_cv']
        widgets = {
            'job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Developer, Data Scientist'
            }),
            'original_cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }

class CVCreationForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}))
    
    class Meta:
        model = CreatedCV
        fields = [
            'full_name', 'email', 'phone', 'address', 'linkedin_url', 'portfolio_url',
            'professional_summary'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your Address'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.com'}),
            'professional_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief professional summary highlighting your key strengths and career objectives...'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' in email and '.' not in email.split('@')[-1]:
            # If email is incomplete, make it valid
            return email + '.com'
        return email
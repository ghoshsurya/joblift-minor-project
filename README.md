# 🚀 JobLift - ATS-Friendly CV Optimizer & Smart Job Hunting Assistant

A comprehensive Django web application that helps job seekers optimize their CVs for Applicant Tracking Systems (ATS) and find relevant job opportunities using AI-powered analysis.

## 👥 Team Members
- **Suryakanta Ghosh** (Roll No. 15571024020)
- **Uttam Kumar Mahto** (Roll No. 15571024001) 
- **Jiten Paramanik** (Roll No. 15571024019)
- **Subhadeep Gorai** (Roll No. 15571024018)

## ✨ Features

### 🔍 CV Analysis & Optimization
- Upload CV in PDF, DOC, or DOCX format
- AI-powered ATS compatibility analysis using Google Gemini
- Get detailed ATS score (0-100%)
- Receive personalized improvement suggestions
- Download optimized ATS-friendly CV

### 💼 Smart Job Search
- Real-time job scraping from multiple portals (Naukri, Indeed, LinkedIn, Monster)
- Advanced filtering by location, job type, and experience
- Get job recommendations based on your profile
- Set up personalized job alerts

### 📊 CV Builder & Templates
- 14+ professional CV templates (Modern, Classic, Creative, Minimal)
- Interactive CV builder with real-time preview
- LaTeX editor for advanced customization
- PDF generation with professional formatting

### 🎯 Additional Features
- Modern admin panel with custom UI
- Dark/Light theme support
- Responsive design for all devices
- Interview preparation resources
- User authentication & profiles
- Real-time search functionality

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (production-ready)
- **Google Gemini AI** - CV analysis and optimization

### Frontend
- **Bootstrap 5.3** - CSS framework
- **JavaScript (ES6+)** - Interactive features
- **Font Awesome** - Icons
- **Custom CSS** - Modern UI/UX

### CV Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **ReportLab** - PDF generation
- **BeautifulSoup** - Web scraping

## 📁 Project Structure

```
MINOR PROJECT/
├── ats_optimizer/          # Main Django project settings
│   ├── __init__.py
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── accounts/               # User authentication & profiles
│   ├── models.py          # CustomUser model
│   ├── views.py           # Auth views
│   ├── forms.py           # User forms
│   ├── urls.py            # Auth URLs
│   └── admin.py           # User admin
│
├── cv_optimizer/           # CV analysis & optimization
│   ├── models.py          # CV, Template, Keyword models
│   ├── views.py           # CV processing views
│   ├── forms.py           # CV forms
│   ├── utils.py           # CV analysis utilities
│   ├── gemini_service.py  # AI analysis service
│   ├── job_matcher.py     # Job matching logic
│   ├── latex_compiler_new.py # LaTeX compilation
│   └── pdf_generator.py   # PDF generation
│
├── job_scraper/           # Job search & scraping
│   ├── models.py          # Job, Portal, Alert models
│   ├── views.py           # Job search views
│   ├── real_scraper.py    # Real-time job scraping
│   ├── api_views.py       # Job search API
│   └── forms.py           # Job search forms
│
├── core/                  # Core functionality & pages
│   ├── models.py          # Hero, Contact, Resource models
│   ├── views.py           # Core page views
│   ├── admin_views.py     # Custom admin views
│   └── urls.py            # Core URLs
│
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── accounts/          # Auth templates
│   ├── cv_optimizer/      # CV templates
│   ├── job_scraper/       # Job search templates
│   ├── core/              # Core page templates
│   └── admin/             # Custom admin templates
│
├── static/                # Static files (CSS, JS, Images)
│   ├── css/style.css      # Main stylesheet
│   └── js/main.js         # Main JavaScript
│
├── media/                 # User uploaded files
│   ├── cvs/original/      # Original CV uploads
│   ├── created_cvs/       # Generated CVs
│   ├── latex_pdfs/        # LaTeX compiled PDFs
│   └── profiles/          # Profile pictures
│
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── db.sqlite3            # SQLite database
├── setup.bat             # Windows setup script
└── start_server.bat      # Server start script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Git installed

### 1. Clone Repository
```bash
git clone https://github.com/ghoshsurya/joblift-minor-project.git
cd joblift-minor-project
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file in root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
GEMINI_API_KEY=your-gemini-api-key
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/

## 🎯 Key Functionalities

### CV Analysis Process
1. **Text Extraction**: Extract text from uploaded CV files
2. **AI Analysis**: Analyze content using Google Gemini AI
3. **ATS Scoring**: Generate compatibility score (0-100%)
4. **Improvement Suggestions**: Provide actionable recommendations
5. **Optimization**: Generate optimized CV content

### Job Scraping
- Real-time scraping from major job portals
- Intelligent filtering and deduplication
- Job matching based on user profile
- Automated job alerts via email

### CV Builder
- Template-based CV creation
- Dynamic form handling for experience/education
- LaTeX compilation for professional output
- PDF generation with custom styling

## 🔧 Configuration

### Gemini AI Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file: `GEMINI_API_KEY=your-key-here`

### Admin Panel Access
- Create superuser: `python manage.py createsuperuser`
- Access at: `/admin/`
- Features: User management, CV analytics, Job monitoring

## 📊 API Endpoints

### CV Operations
- `POST /cv/upload/` - Upload CV for analysis
- `GET /cv/analyze/<id>/` - Get analysis results
- `GET /cv/download/<id>/` - Download optimized CV

### Job Search
- `GET /jobs/search/` - Search jobs with filters
- `POST /jobs/alerts/` - Create job alert
- `GET /api/realtime-search/` - Real-time job search

### User Management
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/profile/` - User profile

## 🎨 UI/UX Features

### Modern Design
- Gradient backgrounds and modern cards
- Smooth animations and transitions
- Responsive grid layouts
- Dark/Light theme support

### Interactive Elements
- Real-time search with instant filtering
- Drag & drop file uploads
- Dynamic form fields
- Progress indicators

### Admin Interface
- Custom admin templates with modern styling
- Enhanced data visualization
- Bulk operations support
- Advanced filtering and search

## 🔒 Security Features

- **CSRF Protection**: All forms protected
- **File Validation**: Secure upload validation
- **User Authentication**: Session-based auth
- **Permission Control**: Role-based access
- **Data Sanitization**: Input validation

## 📈 Performance Optimizations

- **Static File Compression**: Whitenoise integration
- **Database Optimization**: Efficient queries
- **Lazy Loading**: Optimized content loading
- **Caching**: Strategic caching implementation

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in `.env`
2. Configure production database
3. Set up static file serving
4. Configure domain and SSL

### Environment Variables
```env
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
GEMINI_API_KEY=your-gemini-api-key
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📝 License

This project is developed as part of an academic minor project and is intended for educational purposes.

## 📞 Support

For support and queries:
- **Email**: team@joblift.com
- **GitHub Issues**: [Create an issue](https://github.com/ghoshsurya/joblift-minor-project/issues)

## 🏆 Acknowledgments

- Google Gemini AI for CV analysis
- Bootstrap team for UI framework
- Django community for the excellent framework
- All contributors and testers

---

**Made with ❤️ by Team JobLift**

*Empowering job seekers with AI-powered CV optimization and smart job hunting tools.*

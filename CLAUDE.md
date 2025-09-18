# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (Django)
- Create virtual environment: `python -m venv venv && source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run database migrations: `python manage.py migrate`
- Run Django server: `python manage.py runserver` (serves at http://localhost:8000)
- Test: Django tests are in `geogateway_django_app/tests.py` (currently empty)

### Frontend (Vue 3 + Quasar)
- Install dependencies: `cd frontend && npm install` (or `yarn install`)
- Development server: `cd frontend && npm run serve` (runs on port 9000)
- Build production: `cd frontend && npm run build`
- Lint: `cd frontend && npm run lint`

## Architecture Overview

This is a **standalone Django application** with Vue 3 + Quasar frontend. It provides geospatial data visualization and analysis tools and **no longer requires Airavata portal dependencies**.

### Project Structure (3-Project Architecture)
- **geogateway_project/**: Django project configuration
  - `settings.py`: Django settings and configuration
  - `urls.py`: Root URL configuration
  - `wsgi.py`: WSGI application entry point
- **geogateway_django_app/**: Django app (business logic)
  - `views.py`: REST API endpoints and file upload handlers
  - `GeoGatewayData.py`: External API integrations (GPS, UAVSAR, seismicity)
  - `models.py`: Data models for file uploads
  - `urls.py`: URL routing to geospatial services
  - `apps.py`: Django app configuration (standalone)
- **frontend/**: Vue 3 + Quasar frontend application
  - `src/components/`: Vue 3 components for geospatial tools (21 components migrated)
  - `src/store/store.js`: Vuex 4 store for state management
  - `main.js`: Vue 3 app entry point with router configuration
  - Uses Leaflet for mapping, Quasar UI for modern components

### Integration Architecture
- **Standalone Django project** (no Airavata portal required)
- Frontend Vue 3 app runs on port 9000 during development
- Production builds are bundled into Django static files via webpack-bundle-tracker
- Django serves both API endpoints and the built frontend in production
- API endpoints serve geospatial data from external services

### External Services
The app integrates with several geospatial data services:
- GPS/GNSS data from data.geo-gateway.org
- UAVSAR interferometry data
- Seismicity data and earthquake forecasts
- GDACS emergency alerts

### Development Setup Requirements
- **Python 3.8+** and **Node.js 14+** required
- **No external dependencies** - standalone application
- Two terminal workflow: one for Django backend, one for Vue 3 frontend
- Frontend builds automatically integrate with Django via webpack-bundle-tracker

### Technology Stack
- **Backend**: Django 5.2.6 with REST API endpoints
- **Frontend**: Vue 3.5.21 + Quasar UI + Vuex 4 + Vue Router 4
- **Build System**: Vue CLI 5 with webpack integration
- **Security**: All critical vulnerabilities resolved, modern dependency stack

### Migration Status
This project has completed a **comprehensive modernization migration**:
- ✅ **Airavata Removal**: Now standalone (no portal dependency)
- ✅ **Vue 2 → Vue 3**: All 21 components successfully migrated
- ✅ **Bootstrap-Vue → Quasar**: Modern UI library with better security
- ✅ **Security Hardening**: 54% vulnerability reduction achieved
- ✅ **Package Updates**: All dependencies at latest compatible versions

For detailed migration history, see `VUE_MIGRATION.md` and `MIGRATION.md`

## Complete Development Setup Guide

### 1. Clone and Setup
```bash
git clone <repository-url>
cd geogateway-django-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run Django migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install  # or yarn install

# Return to project root
cd ..
```

### 4. Development Workflow

**Terminal 1: Django Backend**
```bash
python manage.py runserver
# Django API available at http://localhost:8000/
```

**Terminal 2: Vue 3 Frontend**
```bash
cd frontend
npm run serve
# Vue development server at http://localhost:9000/
```

### 5. Production Build
```bash
# Build frontend for production
cd frontend
npm run build

# Collect static files (includes Vue bundles)
cd ..
python manage.py collectstatic

# Run Django in production mode
python manage.py runserver --settings=geogateway_project.settings
```

## Deployment Instructions

### Production Deployment Steps

1. **Server Requirements**
   - Python 3.8+ with pip
   - Node.js 14+ with npm
   - Web server (nginx/Apache) for static files
   - Database (SQLite for development, PostgreSQL/MySQL for production)

2. **Application Deployment**
```bash
# Clone repository
git clone <repository-url>
cd geogateway-django-app

# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build frontend
cd frontend
npm install
npm run build

# Configure Django
cd ..
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

3. **Web Server Configuration**
   - Configure nginx/Apache to serve static files from Django's STATIC_ROOT
   - Proxy Django application (typically on port 8000)
   - Set up SSL certificates for production

4. **Environment Variables**
```bash
export DJANGO_SETTINGS_MODULE=geogateway_project.settings
export DEBUG=False
export SECRET_KEY=<your-secret-key>
export DATABASE_URL=<your-database-url>  # if using PostgreSQL
```

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile structure
FROM python:3.11
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/package*.json frontend/
RUN cd frontend && npm install

COPY . .
RUN cd frontend && npm run build
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **Django server won't start**: Check virtual environment is activated and requirements.txt installed
2. **Frontend build fails**: Ensure Node.js 14+ is installed, run `npm install` in frontend directory
3. **Static files not loading**: Run `python manage.py collectstatic` after frontend build
4. **API calls failing**: Check CORS settings in Django settings.py
5. **Vue components not rendering**: Ensure webpack-bundle-tracker integration is working

### Development Tips

- Use `python manage.py check` to verify Django configuration
- Use `npm run lint` in frontend directory to check Vue code quality
- Monitor both Django and frontend logs during development
- Use browser dev tools to debug Vue 3 components (Vue DevTools extension)

### Performance Optimization

- **Frontend**: Consider code splitting with Vue Router lazy loading
- **Backend**: Implement database query optimization and caching
- **Static Files**: Use CDN for static file serving in production
- **Bundle Analysis**: Use `npm run build --report` to analyze bundle sizes
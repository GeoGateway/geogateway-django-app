# GeoGateway Django App

A standalone Django application for geospatial data visualization and analysis tools, built with Django backend and Vue 3 + Quasar frontend.

## Requirements

- Python 3.8 or later
- Node.js 14 or later (required for Vue 3 + Quasar)
- yarn or npm

## Architecture

This application uses a **three-project architecture** for separation of concerns and standalone deployment:

- **Backend**: Django 4.2+ with REST API endpoints for geospatial data services
- **Frontend**: Vue 3.5+ with Quasar UI framework for responsive components
- **Integration**: webpack-bundle-tracker for Django + Vue 3 integration
- **Data Sources**: GPS/GNSS, UAVSAR, seismicity, and emergency alert services

### Project Structure

```
geogateway-django-app/
├── frontend/                    # Vue 3 + Quasar Frontend Project
│   ├── src/components/          # Vue components (GNSS, UAVSAR, MapTools, etc.)
│   ├── src/store/              # Vuex state management
│   ├── package.json            # Frontend dependencies
│   └── vue.config.js           # Vue CLI configuration
│
├── geogateway_django_app/       # Django Application (Business Logic)
│   ├── GeoGatewayData.py       # External API integrations
│   ├── views.py                # REST API endpoints
│   ├── models.py               # Data models
│   ├── urls.py                 # URL routing
│   └── migrations/             # Database migrations
│
├── geogateway_project/          # Django Project (Configuration)
│   ├── settings.py             # Django settings & configuration
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI application entry point
│   └── asgi.py                 # ASGI application entry point
│
├── manage.py                   # Django management commands
├── requirements.txt            # Python dependencies
└── setup.py                    # Package installation & frontend build
```

### Architecture Flow

```
Browser Request
    ↓
Django Project (geogateway_project/)
    ├── settings.py (webpack_loader, static files config)
    ├── urls.py (routes to geogateway_django_app.urls)
    └── WSGI/ASGI servers
    ↓
Django App (geogateway_django_app/)
    ├── REST API endpoints (/api/gnss, /api/uavsar, etc.)
    ├── File upload handlers
    └── External service integrations
    ↓
Static Files (from frontend/)
    ├── Vue 3 + Quasar compiled bundles
    ├── webpack-bundle-tracker integration
    └── Single-page application
```

### Why Three Projects?

This architecture evolved from the **Airavata migration** to create a standalone application:

**Before (2-Project Plugin)**:
- `frontend/` - Vue.js interface
- `geogateway_django_app/` - Django app plugin for Airavata portal

**After (3-Project Standalone)**:
- `frontend/` - Vue 3 + Quasar interface
- `geogateway_django_app/` - Django app (business logic)
- `geogateway_project/` - Django project (standalone configuration)

**Benefits**:
- **Separation of Concerns**: Clear boundaries between configuration, business logic, and UI
- **Standalone Deployment**: No longer requires Airavata portal infrastructure
- **Maintainability**: Independent project components with defined responsibilities
- **Reusability**: Django app can be installed in other projects if needed

## Setting up the development environment

### Prerequisites
- Python 3.8 or later
- Node.js 14 or later
- npm or yarn package manager

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
# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install  # or yarn install
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
npm run serve  # or yarn serve
# Vue development server at http://localhost:9000/
```

### 5. Access the application
- Django API: http://localhost:8000/
- Vue 3 frontend: http://localhost:9000/
- Main app: http://localhost:8000/ (Django serves the built frontend in production)

**Note**: The frontend uses Vue 3.5+ with Quasar UI framework for modern, secure components and enhanced performance.

## Production Build

```bash
# Build Vue 3 frontend for production (generates optimized bundles)
cd frontend
npm run build  # or yarn build

# Collect static files (includes Vue 3 bundles and assets)
cd ..
python manage.py collectstatic

# Run Django in production mode
python manage.py runserver --settings=geogateway_project.settings
```

**Vue 3 Build Output**: The build process generates optimized JavaScript and CSS bundles in `frontend/dist/` which are automatically integrated with Django via webpack-bundle-tracker.

## Deployment

### Production Deployment

1. **Server Requirements**
   - Python 3.8+ with pip
   - Node.js 14+ with npm
   - Web server (nginx/Apache) for static file serving
   - Database (SQLite for development, PostgreSQL/MySQL for production)

2. **Deployment Steps**
```bash
# Clone and setup
git clone <repository-url>
cd geogateway-django-app

# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build frontend
cd frontend
npm install
npm run build

# Django setup
cd ..
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

3. **Environment Configuration**
```bash
export DJANGO_SETTINGS_MODULE=geogateway_project.settings
export DEBUG=False
export SECRET_KEY=<your-production-secret-key>
export DATABASE_URL=<your-database-url>  # if using PostgreSQL
```

4. **Web Server Setup**
   - Configure nginx/Apache to serve static files from Django's STATIC_ROOT
   - Proxy requests to Django application (typically port 8000)
   - Set up SSL certificates for HTTPS

For detailed deployment instructions and troubleshooting, see `CLAUDE.md`.

## Available Commands

### Backend
- `python manage.py runserver` - Start Django development server
- `python manage.py migrate` - Run database migrations
- `python manage.py test` - Run tests
- `python manage.py collectstatic` - Collect static files

### Frontend
- `npm run serve` - Start Vue 3 development server with hot module replacement
- `npm run build` - Build Vue 3 + Quasar for production (optimized bundles)
- `npm run lint` - Run ESLint for Vue 3 and JavaScript code quality

## Technology Stack

### Frontend Project (`frontend/`)
- **Vue 3.5+**: Modern reactive framework with Composition API support
- **Quasar UI**: Material Design components (replaces Bootstrap-Vue)
- **Vue Router 4**: Client-side routing for single-page application
- **Vuex 4**: State management for complex application state
- **Leaflet**: Interactive maps for geospatial data visualization
- **Webpack**: Module bundler with Django integration via webpack-bundle-tracker

### Django Project (`geogateway_project/`)
- **Django 4.2+**: Web framework configuration and project settings
- **webpack-loader**: Integration with Vue 3 frontend bundles
- **Static Files**: Serves production Vue 3 builds
- **WSGI/ASGI**: Production deployment interfaces

### Django App (`geogateway_django_app/`)
- **Django REST Framework**: API development for frontend integration
- **GeoPy/GDAL**: Geospatial data processing libraries
- **File Upload**: Handles KML/KMZ file processing
- **External APIs**: Integration layer for geospatial services

### External Services
- **GPS/GNSS Data**: Real-time positioning data from data.geo-gateway.org
- **UAVSAR**: Radar interferometry data for ground deformation analysis
- **Seismicity APIs**: Earthquake data and emergency alerts (GDACS)

## Security & Performance

- ✅ **Security Updates**: Vue 3 migration resolved ReDoS and XSS vulnerabilities
- ✅ **Modern Dependencies**: All packages updated to latest secure versions
- ✅ **Performance**: Vue 3 provides improved bundle sizes and rendering speed
- ✅ **Mobile-Responsive**: Quasar UI ensures cross-device compatibility

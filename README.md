# GeoGateway Django App

A search and analysis gateway to geodetic imaging data for scientific discovery, field use and disaster response

## Table of Contents

- [Requirements](#requirements)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended-for-quick-setup)
  - [Option 2: Local Development](#option-2-local-development)
- [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Architecture Flow](#architecture-flow)
  - [Why Three Projects?](#why-three-projects)
- [Setting up the development environment](#setting-up-the-development-environment)
  - [Prerequisites](#prerequisites)
  - [1. Clone and Setup](#1-clone-and-setup)
  - [2. Database Setup](#2-database-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Development Workflow](#4-development-workflow)
  - [5. Access the application](#5-access-the-application)
- [🐳 Docker Setup (Recommended)](#-docker-setup-recommended)
  - [Quick Start with Docker](#quick-start-with-docker)
  - [What Gets Started](#what-gets-started)
  - [Docker Commands](#docker-commands)
  - [Environment Configuration](#environment-configuration)
  - [Production Docker Deployment](#production-docker-deployment)
  - [Building Custom Images](#building-custom-images)
  - [Docker Troubleshooting](#docker-troubleshooting)
    - [Common Issues and Solutions](#common-issues-and-solutions)
    - [Performance Tips](#performance-tips)
    - [Getting Help](#getting-help)
- [Production Build (Local Development)](#production-build-local-development)
- [Deployment](#deployment)
  - [Recommended: Docker Production Deployment](#recommended-docker-production-deployment)
  - [Alternative: Manual Production Deployment](#alternative-manual-production-deployment)
- [Available Commands](#available-commands)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Technology Stack](#technology-stack)
  - [Frontend Project](#frontend-project-frontend)
  - [Django Project](#django-project-geogateway_project)
  - [Django App](#django-app-geogateway_django_app)
  - [External Services](#external-services)

## Requirements

### Option 1: Docker (Recommended for quick setup)
- Docker 20.10+ and Docker Compose v2
- 4GB+ RAM available for containers

### Option 2: Local Development
- Python 3.8 or later
- Node.js 22+ LTS (required for Vue 3 + Quasar)
- yarn or npm

## Architecture

This application uses a **three-project architecture** for separation of concerns and standalone deployment:

- **Backend**: Django 5.2.6+ with REST API endpoints for geospatial data services
- **Frontend**: Vue 3.5+ with Quasar UI framework for responsive components
- **Integration**: webpack-bundle-tracker for Django + Vue 3 integration
- **Data Sources**: GPS/GNSS, UAVSAR, seismicity, and emergency alert services

### Project Structure

```
geogateway-django-app/
├── frontend/                   # Vue 3 + Quasar Frontend Project
│   ├── src/components/         # Vue components (GNSS, UAVSAR, MapTools, etc.)
│   ├── src/store/              # Vuex state management
│   ├── package.json            # Frontend dependencies
│   └── vue.config.js           # Vue CLI configuration
│
├── geogateway_django_app/      # Django Application (Business Logic)
│   ├── GeoGatewayData.py       # External API integrations
│   ├── views.py                # REST API endpoints
│   ├── models.py               # Data models
│   ├── urls.py                 # URL routing
│   └── migrations/             # Database migrations
│
├── geogateway_project/         # Django Project (Configuration)
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

- `frontend/` - Vue 3 + Quasar interface
- `geogateway_django_app/` - Django app (business logic)
- `geogateway_project/` - Django project (standalone configuration)

**Benefits**:
- **Separation of Concerns**: Clear boundaries between configuration, business logic, and UI
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

## 🐳 Docker Setup (Recommended)

### Quick Start with Docker

The fastest way to get the application running is with Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd geogateway-django-app

# Start the entire application stack
docker-compose up -d

# Wait for services to be ready (about 30-60 seconds)
# Check status
docker-compose ps

# Access the application
# - Full app: http://localhost (via Nginx)
# - Django API: http://localhost:8000 (direct access)
```

### What Gets Started

The Docker setup includes:
- **Web Service**: Django app with Vue.js frontend built-in
- **Nginx**: Reverse proxy for static files and load balancing
- **Volumes**: Persistent storage for SQLite database, static files, and media

### Docker Commands

```bash
# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f web

# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput

# Access the web container shell
docker-compose exec web bash

# Stop all services
docker-compose down

# Stop and remove all data (⚠️ destructive)
docker-compose down -v
```

### Environment Configuration

For production or custom configuration, copy and modify the environment file:

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional)
nano .env
```

Key environment variables:
- `DEBUG=0` - Disable debug mode for production
- `SECRET_KEY=your-secret-key` - Django secret key
- `ALLOWED_HOSTS=yourdomain.com,localhost` - Allowed hostnames

### Production Docker Deployment

For production environments, use the production Docker Compose file:

```bash
# Production deployment with SSL and optimized settings
docker-compose -f docker-compose.prod.yml up -d

# Run initial setup
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Building Custom Images

If you need to modify the Docker image:

```bash
# Build only the web service
docker-compose build web

# Build with no cache (fresh build)
docker-compose build --no-cache web

# Build and start
docker-compose up --build -d
```

### Docker Troubleshooting

#### Common Issues and Solutions

**1. Port Already in Use**
```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :80

# Stop conflicting services or change ports in docker-compose.yml
# Kill specific processes
sudo kill -9 <PID>
```

**2. Database Connection Issues**
```bash
# Wait for database to be ready
docker-compose logs db

# Check database status
docker-compose exec db pg_isready -U geogateway

# Reset database (⚠️ loses all data)
docker-compose down -v
docker-compose up -d
```

**3. Frontend Build Failures**
```bash
# Check Node.js version in container
docker-compose exec web node --version

# Clear npm cache and rebuild
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
```

**4. Permission Issues**
```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .

# On Windows with WSL2, ensure proper line endings
git config --global core.autocrlf false
```

**5. Container Health Issues**
```bash
# Check container health
docker-compose ps
docker-compose top

# Restart specific service
docker-compose restart web

# View detailed logs
docker-compose logs --details web
```

**6. Out of Disk Space**
```bash
# Clean up Docker resources
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk usage
docker system df
```

#### Performance Tips

- **Increase Memory**: Ensure Docker has at least 4GB RAM allocated
- **Use SSD**: Store Docker volumes on SSD for better database performance
- **Disable Antivirus**: Exclude project directory from real-time scanning
- **Update Docker**: Use latest Docker Desktop version for performance improvements

#### Getting Help

If you encounter issues:

1. Check the container logs: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Test database connectivity: `docker-compose exec db pg_isready`
4. Ensure all required ports are available: `netstat -tulpn | grep :80`

## Production Build (Local Development)

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

### Recommended: Docker Production Deployment

**The easiest production deployment method is using Docker:**

```bash
# Clone repository on your server
git clone <repository-url>
cd geogateway-django-app

# Configure environment
cp .env.example .env
# Edit .env with your production settings

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Run initial setup
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

**Production URLs:**
- Application: https://yourdomain.com (via Nginx with SSL)
- Admin: https://yourdomain.com/admin

### Alternative: Manual Production Deployment

1. **Server Requirements**
   - Python 3.8+ with pip
   - Node.js 22+ LTS with npm
   - Web server (nginx/Apache) for static file serving

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

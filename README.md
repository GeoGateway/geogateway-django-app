# GeoGateway Django App

A standalone Django application for geospatial data visualization and analysis tools.

## Requirements

- Python 3.8 or later
- Node.js 14 or later
- yarn or npm

## Setting up the development environment

### 1. Clone the repository
```bash
git clone <repository-url>
cd geogateway-django-app
```

### 2. Backend Setup (Django)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

### 3. Frontend Setup (Vue.js)
Open a new terminal window:
```bash
cd frontend

# Install dependencies
yarn install
# or: npm install

# Start development server
yarn serve
# or: npm run serve
```

### 4. Access the application
- Django API: http://localhost:8000/
- Vue.js frontend: http://localhost:9000/
- Main app: http://localhost:8000/ (Django serves the built frontend in production)

## Production Build

```bash
# Build frontend for production
cd frontend
yarn build

# Collect static files
python manage.py collectstatic

# Run Django with production settings
python manage.py runserver --settings=geogateway_project.settings_prod
```

## Available Commands

### Backend
- `python manage.py runserver` - Start Django development server
- `python manage.py migrate` - Run database migrations
- `python manage.py test` - Run tests
- `python manage.py collectstatic` - Collect static files

### Frontend
- `yarn serve` - Start Vue.js development server
- `yarn build` - Build for production
- `yarn lint` - Run ESLint

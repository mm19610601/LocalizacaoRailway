# Sistema de Rastreamento - Location Tracking System

## Overview

This is a Flask-based location tracking web application built in Portuguese that allows organizations to track and manage user locations in real-time. The system provides a comprehensive dashboard with interactive maps, user management, and location history tracking capabilities.

**Current Status (July 25, 2025):** System fully functional and connected to Railway PostgreSQL database. Ready for permanent deployment to Railway platform for 24/7 online access.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Database**: PostgreSQL (configured via DATABASE_URL environment variable)
- **Session Management**: Flask built-in sessions with configurable secret key
- **Proxy Support**: Werkzeug ProxyFix middleware for deployment behind reverse proxies

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme (Replit-themed)
- **Interactive Maps**: Leaflet.js for map visualization
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JavaScript for map interactions and filtering

### Data Storage
- **Primary Database**: PostgreSQL with automatic URL conversion from Heroku format
- **Connection Pooling**: Configured with pool_recycle and pool_pre_ping for reliability
- **Database Models**: Two main entities (Users and Locations) with foreign key relationships

## Key Components

### Models (models.py)
1. **Utilizador (User)**
   - Primary user entity with authentication fields
   - Stores user profile information (name, role, phone)
   - One-to-many relationship with locations

2. **Localizacao (Location)**
   - GPS coordinates with precision data
   - Timestamped location entries
   - Foreign key relationship to users
   - Serialization method for JSON API responses

### Routes (routes.py)
1. **Dashboard Route** (`/`)
   - Main interface with map visualization
   - Recent locations filtering (last 24 hours)
   - User selection dropdown

2. **User Management** (`/users`)
   - CRUD operations for user accounts
   - User statistics display

3. **Location Management** (`/locations`)
   - Location history with filtering capabilities
   - Date range and user-specific filtering

### Frontend Templates
1. **Base Template** - Common layout with Bootstrap navigation
2. **Index Template** - Dashboard with map and filters
3. **Users Template** - User management interface
4. **Locations Template** - Location history and filtering

### Static Assets
1. **CSS** - Custom styling for map markers and UI elements
2. **JavaScript** - Map initialization and interaction logic

## Data Flow

1. **Location Data Input**: GPS coordinates stored with user association and timestamp
2. **Data Processing**: Flask routes query SQLAlchemy models with filtering capabilities
3. **Map Visualization**: Locations converted to JSON and rendered on Leaflet maps
4. **User Interaction**: Filters applied via JavaScript to update map displays
5. **Database Persistence**: All data stored in PostgreSQL with relationship integrity

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- SQLAlchemy (database toolkit)
- Werkzeug (WSGI utilities)

### Frontend Libraries
- Bootstrap 5 with Replit dark theme
- Leaflet.js (interactive maps)
- Font Awesome (icons)
- OpenStreetMap tiles (map imagery)

### Database
- PostgreSQL (production database)
- Environment-based configuration via DATABASE_URL

## Deployment Strategy

### Environment Configuration
- **DATABASE_URL**: PostgreSQL connection string (auto-converted from Heroku format)
- **SESSION_SECRET**: Flask session encryption key
- **Development**: Default configurations for local development

### Production Considerations
- ProxyFix middleware enabled for reverse proxy deployment
- Connection pooling configured for database reliability
- Automatic table creation on application startup
- Error logging and exception handling throughout

### Scalability Features
- Database connection pooling
- Efficient query patterns with SQLAlchemy
- Paginated location displays
- Client-side filtering to reduce server load

The system is designed for organizational use cases where tracking employee or asset locations is required, with a focus on real-time visualization and historical data analysis.
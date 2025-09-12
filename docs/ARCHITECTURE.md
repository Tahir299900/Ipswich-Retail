# Ipswich Retail - System Architecture

## Overview
Ipswich Retail e-commerce application built using Django Model-View-Template (MVT) architecture following DevOps best practices.

## Architecture Components

### 1. Django MVT Architecture
- **Models**: Data layer (Product, Category, Order, User Profile)
- **Views**: Business logic layer (Product listing, Cart management, Order processing)
- **Templates**: Presentation layer (HTML templates with Bootstrap styling)

### 2. Application Structure
```
ipswich_retail/
├── store/                    # Main e-commerce app
│   ├── models.py            # Data models
│   ├── views.py             # Business logic
│   ├── urls.py              # URL routing
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── templates/               # Shared templates
├── static/                  # Global static files
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-service setup
└── .github/workflows/      # CI/CD pipelines
```

### 3. DevOps Pipeline Architecture

#### Development → Staging → Production Flow
1. **Code Commit** → GitHub repository
2. **Automated Testing** → GitHub Actions
3. **Build & Containerization** → Docker
4. **Deployment** → Render.com/Railway
5. **Monitoring** → Application logs & health checks

### 4. Key Features
- **Product Catalog**: Browse and search products
- **Shopping Cart**: Session-based cart management
- **User Authentication**: Registration, login, profile management
- **Order Processing**: Checkout and order history
- **Admin Interface**: Product and order management

### 5. DevOps Practices Implemented
- **Version Control**: Git with feature branching
- **Containerization**: Docker for consistent environments
- **CI/CD**: Automated testing and deployment
- **Infrastructure as Code**: Docker Compose configuration
- **Monitoring**: Application logging and health checks
- **Security**: Environment variable management

## Database Schema
- **User**: Extended Django User model
- **Category**: Product categorization
- **Product**: Main product information
- **Cart**: Session-based shopping cart
- **Order**: Customer orders
- **OrderItem**: Individual items in orders

## Technology Stack
- **Backend**: Django 5.2.6
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render.com or Railway
- **Monitoring**: Django logging system
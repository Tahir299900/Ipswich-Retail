# Deployment Guide - Ipswich Retail

This guide covers deploying the Ipswich Retail e-commerce platform to various production environments.

## 🚀 Quick Deployment Options

### 1. Render.com (Recommended)
**Best for: Easy deployment with minimal configuration**

1. **Fork the repository** to your GitHub account
2. **Connect to Render.com**:
   - Visit [render.com](https://render.com)
   - Connect your GitHub account
   - Select the Ipswich Retail repository

3. **Configure the deployment**:
   - Service Type: Web Service
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `python manage.py migrate && python manage.py populate_store && gunicorn ipswich_retail.wsgi:application`

4. **Set environment variables**:
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=postgresql://... # Auto-provided by Render
   ```

5. **Add PostgreSQL database**:
   - Go to Dashboard > New > PostgreSQL
   - Connect to your web service

### 2. Railway (Alternative)
**Best for: Simple container deployment**

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy from repository**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add database**:
   ```bash
   railway add postgresql
   ```

### 3. Docker Compose (Self-hosted)
**Best for: Full control and on-premises deployment**

1. **Prepare the server**:
   ```bash
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo pip install docker-compose
   ```

2. **Clone and configure**:
   ```bash
   git clone https://github.com/Tahir299900/Ipswich-Retail.git
   cd Ipswich-Retail
   cp .env.production .env
   # Edit .env with your configuration
   ```

3. **Deploy**:
   ```bash
   chmod +x scripts/deploy.sh
   PLATFORM=docker-compose ./scripts/deploy.sh
   ```

## 🔧 Detailed Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-long-random-secret-key` |
| `DEBUG` | Debug mode (False for production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection (optional) | `redis://localhost:6379` |

### Database Setup

#### PostgreSQL Configuration
```sql
-- Create database and user
CREATE DATABASE ipswich_retail;
CREATE USER ipswich_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ipswich_retail TO ipswich_user;
```

#### Migration Commands
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py populate_store
```

### SSL/HTTPS Setup

#### Using Traefik (Docker Compose)
The production Docker Compose includes Traefik for automatic SSL:
```yaml
traefik:
  image: traefik:v2.10
  command:
    - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
    - "--certificatesresolvers.letsencrypt.acme.email=your-email@domain.com"
```

#### Manual SSL Setup
1. **Obtain SSL certificate** (Let's Encrypt recommended)
2. **Configure nginx** or your load balancer
3. **Update Django settings**:
   ```python
   SECURE_SSL_REDIRECT = True
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   ```

## 📊 Monitoring Setup

### Health Checks
The application provides health check endpoints:
- **Health**: `/health/` - Overall application health
- **Readiness**: `/ready/` - Deployment readiness

### Prometheus Metrics (Optional)
For advanced monitoring, the production setup includes Prometheus:
```bash
# Access Prometheus dashboard
http://your-domain:9090

# Access Grafana dashboard
http://your-domain:3000
# Default login: admin / (check GRAFANA_PASSWORD env var)
```

### Log Monitoring
Application logs are configured in Django settings:
```python
LOGGING = {
    'handlers': {
        'file': {'filename': '/app/logs/django.log'},
        'console': {'class': 'logging.StreamHandler'},
    }
}
```

## 🔒 Security Configuration

### Production Security Checklist

- [ ] **SECRET_KEY**: Generate a new, secure secret key
- [ ] **DEBUG**: Set to `False`
- [ ] **ALLOWED_HOSTS**: Specify your domains only
- [ ] **HTTPS**: Enable SSL/TLS encryption
- [ ] **Database**: Use strong passwords
- [ ] **Static Files**: Serve via CDN (recommended)
- [ ] **Environment Variables**: Store secrets securely
- [ ] **Updates**: Keep dependencies updated

### Security Headers
Django security middleware is configured:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check WhiteNoise configuration
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

#### 2. Database Connection Issues
```bash
# Test database connection
python manage.py dbshell

# Check DATABASE_URL format
DATABASE_URL=postgresql://username:password@hostname:5432/database
```

#### 3. Health Check Failures
```bash
# Test health endpoint
curl -f http://localhost:8000/health/

# Check application logs
docker logs container_name
```

#### 4. Permission Denied (Docker)
```bash
# Fix file permissions
chmod +x scripts/deploy.sh

# Check Docker daemon
sudo systemctl status docker
```

### Debug Commands

```bash
# Check Django configuration
python manage.py check --deploy

# View migration status
python manage.py showmigrations

# Test email configuration
python manage.py sendtestemail user@example.com

# Check static files
python manage.py findstatic admin/css/base.css
```

## 📈 Performance Optimization

### Database Optimization
```python
# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
        },
    }
}
```

### Caching Setup
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
    }
}
```

### Static File CDN
```python
# AWS S3 for static files (optional)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
```

## 🔄 CI/CD Integration

### GitHub Actions Deployment
The repository includes a complete CI/CD pipeline:
```yaml
# .github/workflows/ci.yml
- name: Deploy to production
  if: github.ref == 'refs/heads/master'
  run: |
    # Deployment commands
```

### Manual Deployment
```bash
# Build and deploy manually
docker build -t ipswich-retail .
docker tag ipswich-retail your-registry/ipswich-retail
docker push your-registry/ipswich-retail
```

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/Tahir299900/Ipswich-Retail/issues)
- **Documentation**: Check `/docs` folder
- **Health Checks**: Monitor `/health/` endpoint

### Monitoring Checklist
- [ ] Application responds to health checks
- [ ] Database connectivity verified
- [ ] Static files loading correctly
- [ ] SSL certificate valid
- [ ] Performance metrics within targets
- [ ] Logs are being collected
- [ ] Backup strategy in place

---

**🎉 Congratulations! Your Ipswich Retail application is now deployed and ready for production traffic.**
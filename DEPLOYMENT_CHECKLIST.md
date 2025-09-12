# 🚀 Production Deployment Checklist

## Pre-Deployment Requirements

### ✅ Code Quality & Testing
- [ ] All tests passing (run `python manage.py test`)
- [ ] Code quality checks passed (`black`, `flake8`, `isort`)
- [ ] Security scan completed (`bandit`, `safety`)
- [ ] Django deployment checks passed (`python manage.py check --deploy`)
- [ ] Static files collected successfully
- [ ] Database migrations applied

### ✅ Configuration
- [ ] Production settings configured (`production_settings.py`)
- [ ] Environment variables set (see `.env.production`)
- [ ] Database URL configured
- [ ] Secret key generated (50+ characters)
- [ ] Allowed hosts configured
- [ ] SSL/HTTPS settings enabled
- [ ] Debug mode disabled (`DEBUG=False`)

### ✅ Infrastructure
- [ ] Database server ready (PostgreSQL recommended)
- [ ] Redis server configured (optional but recommended)
- [ ] SSL certificate obtained
- [ ] Domain name configured
- [ ] Load balancer configured (if applicable)

## Deployment Steps

### 1. Platform Selection
Choose your deployment platform:
- [ ] **Render.com** (Recommended for beginners)
- [ ] **Railway** (Good Docker support)
- [ ] **DigitalOcean App Platform** (Scalable)
- [ ] **Self-hosted with Docker** (Full control)

### 2. Render.com Deployment
1. [ ] Fork repository to your GitHub account
2. [ ] Create Render account and connect GitHub
3. [ ] Create new Web Service from repository
4. [ ] Configure build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
5. [ ] Configure start command: `python manage.py migrate && python manage.py populate_store && gunicorn ipswich_retail.wsgi:application`
6. [ ] Add PostgreSQL database
7. [ ] Set environment variables:
   ```
   SECRET_KEY=<generated-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=<auto-populated-by-render>
   ```
8. [ ] Deploy and verify

### 3. Railway Deployment
1. [ ] Install Railway CLI: `npm install -g @railway/cli`
2. [ ] Login: `railway login`
3. [ ] Initialize project: `railway init`
4. [ ] Add PostgreSQL: `railway add postgresql`
5. [ ] Deploy: `railway up`

### 4. Docker Self-Hosted Deployment
1. [ ] Clone repository to server
2. [ ] Configure environment: `cp .env.production .env`
3. [ ] Build and deploy: `./scripts/deploy.sh`
4. [ ] Configure reverse proxy (nginx/traefik)
5. [ ] Set up SSL certificate

## Post-Deployment Verification

### ✅ Application Health
- [ ] Application loads successfully
- [ ] Health endpoint responding: `GET /health/`
- [ ] Readiness endpoint responding: `GET /ready/`
- [ ] Database connection working
- [ ] Static files loading correctly
- [ ] Admin interface accessible

### ✅ Functionality Testing
- [ ] User registration/login working
- [ ] Product catalog displays correctly
- [ ] Shopping cart functionality works
- [ ] Checkout process completes successfully
- [ ] Order history displays correctly
- [ ] Admin can manage products and orders

### ✅ Security Verification
- [ ] HTTPS enabled and working
- [ ] SSL certificate valid
- [ ] Security headers present
- [ ] No debug information exposed
- [ ] Admin interface secured

### ✅ Performance & Monitoring
- [ ] Page load times acceptable (<2 seconds)
- [ ] Database queries optimized
- [ ] Static files served efficiently
- [ ] Error logging working
- [ ] Health monitoring setup

## Environment Variables Reference

### Required Variables
```bash
SECRET_KEY=<50-character-random-string>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Optional Variables
```bash
REDIS_URL=redis://host:6379
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SENTRY_DSN=https://your-sentry-dsn
```

## Troubleshooting Common Issues

### Issue: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput --clear
# Check STATICFILES_STORAGE setting
```

### Issue: Database Connection Failed
**Solution:**
```bash
# Verify DATABASE_URL format
# Test connection: python manage.py dbshell
```

### Issue: 500 Internal Server Error
**Solution:**
```bash
# Check application logs
# Verify all environment variables are set
# Run: python manage.py check --deploy
```

### Issue: Health Check Failing
**Solution:**
```bash
# Test locally: curl http://localhost:8000/health/
# Check database connectivity
# Verify static files are accessible
```

## Rollback Plan

### If Deployment Fails:
1. [ ] Revert to previous Docker image/tag
2. [ ] Restore database from backup (if needed)
3. [ ] Update DNS if necessary
4. [ ] Verify rollback successful
5. [ ] Investigate and fix issues
6. [ ] Re-deploy when ready

## Monitoring Setup

### Health Monitoring
- [ ] Set up uptime monitoring (Pingdom, UptimeRobot)
- [ ] Configure health check alerts
- [ ] Set up error rate monitoring
- [ ] Monitor database performance

### Log Aggregation
- [ ] Configure centralized logging
- [ ] Set up log rotation
- [ ] Configure error alerts
- [ ] Monitor application metrics

## Success Criteria

### ✅ Deployment Complete When:
- [ ] Application accessible via HTTPS
- [ ] All functionality tested and working
- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] Performance metrics acceptable
- [ ] Security scan clean
- [ ] Team notified of successful deployment

---

## 🎉 Deployment Complete!

**Live Application:** https://your-domain.com
**Admin Panel:** https://your-domain.com/admin/
**Health Check:** https://your-domain.com/health/

### Next Steps:
1. Monitor application performance
2. Set up regular backups
3. Plan for scaling if needed
4. Update documentation with live URLs
5. Celebrate successful DevOps implementation! 🎊
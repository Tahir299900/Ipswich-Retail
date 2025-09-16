# Render Deployment Guide for Ipswich Retail

## Prerequisites
- GitHub repository connected to Render
- Render account (free tier works)

## Steps to Deploy

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin develop
```

### 2. Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository (already connected)
4. Configure the service:
   - **Name**: `ipswich-retail`
   - **Region**: Choose closest to your users
   - **Branch**: `develop` (or `master` for production)
   - **Runtime**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn ipswich_retail.wsgi:application`

### 3. Set Environment Variables

In the Render dashboard, add these environment variables:

| Variable | Value |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `ipswich_retail.settings.production` |
| `PYTHON_VERSION` | `3.11.0` |
| `WEB_CONCURRENCY` | `4` |
| `SECRET_KEY` | Click "Generate" for a secure random key |

### 4. Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `ipswich-retail-db`
   - **Database**: `ipswich_retail`
   - **User**: `ipswich_retail`
   - **Region**: Same as your web service
3. Click "Create Database"
4. Copy the Internal Database URL

### 5. Connect Database to Web Service

1. Go back to your web service
2. In Environment Variables, add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from step 4

### 6. Deploy

1. Click "Manual Deploy" → "Deploy latest commit"
2. Watch the build logs
3. Once deployed, your app will be available at:
   `https://ipswich-retail.onrender.com`

## File Structure Created

```
devops/
├── render.yaml              # Render configuration file
├── build.sh                 # Build script for deployment
├── requirements.txt         # Updated Python dependencies
├── ipswich_retail/
│   └── settings/
│       └── production.py    # Production settings
└── RENDER_DEPLOYMENT.md     # This guide
```

## Important Notes

1. **Free Tier Limitations**:
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - Limited build hours per month

2. **Static Files**:
   - Handled by WhiteNoise middleware
   - Automatically compressed and cached

3. **Database Backups**:
   - Free tier includes daily backups
   - Can be restored from Render dashboard

4. **Custom Domain**:
   - Can add custom domain in Settings
   - SSL certificate automatically provided

## Monitoring

- Check build logs in Render dashboard
- View application logs in "Logs" tab
- Monitor metrics in "Metrics" tab

## Troubleshooting

### Build Fails
- Check `requirements.txt` for correct versions
- Ensure `build.sh` has correct permissions
- Review build logs for specific errors

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Ensure database credentials match

### Static Files Not Loading
- Run `python manage.py collectstatic` locally
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise middleware is installed

## Next Steps

1. Set up automatic deployments from GitHub
2. Configure custom domain
3. Set up monitoring alerts
4. Consider upgrading to paid tier for:
   - Always-on service
   - More build minutes
   - Better performance
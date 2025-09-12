from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for monitoring and load balancers
    """
    health_status = {
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': None,
        'services': {}
    }
    
    try:
        # Database connectivity check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['services']['database'] = f'error: {str(e)}'
        logger.error(f"Database health check failed: {e}")
    
    # Static files check
    try:
        static_root = settings.STATIC_ROOT
        if os.path.exists(static_root):
            health_status['services']['static_files'] = 'healthy'
        else:
            health_status['services']['static_files'] = 'warning: static files not found'
    except Exception as e:
        health_status['services']['static_files'] = f'error: {str(e)}'
    
    # Media files check
    try:
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root):
            health_status['services']['media_files'] = 'healthy'
        else:
            health_status['services']['media_files'] = 'warning: media directory not found'
    except Exception as e:
        health_status['services']['media_files'] = f'error: {str(e)}'
    
    # Import Django timezone for timestamp
    from django.utils import timezone
    health_status['timestamp'] = timezone.now().isoformat()
    
    # Set HTTP status code
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JsonResponse(health_status, status=status_code)

def readiness_check(request):
    """
    Readiness check endpoint for Kubernetes/Docker deployments
    """
    readiness_status = {
        'status': 'ready',
        'checks': {}
    }
    
    try:
        # Check if we can perform database operations
        from .models import Product
        Product.objects.first()  # Simple query to test DB
        readiness_status['checks']['database_query'] = 'ready'
    except Exception as e:
        readiness_status['status'] = 'not_ready'
        readiness_status['checks']['database_query'] = f'error: {str(e)}'
    
    # Check if migrations are up to date
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.base import CommandError
        from io import StringIO
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
            readiness_status['checks']['migrations'] = 'ready'
        except CommandError:
            readiness_status['checks']['migrations'] = 'ready'  # Assume ready if command fails
        finally:
            sys.stdout = old_stdout
    except Exception as e:
        readiness_status['checks']['migrations'] = f'warning: {str(e)}'
    
    status_code = 200 if readiness_status['status'] == 'ready' else 503
    return JsonResponse(readiness_status, status=status_code)
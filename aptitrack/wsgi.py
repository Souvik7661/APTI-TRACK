"""
WSGI config for AptiTrack project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aptitrack.settings')
application = get_wsgi_application()

# Auto-initialize ephemeral SQLite DB on Vercel cold starts
if os.environ.get('VERCEL') == '1' and not os.environ.get('DATABASE_URL') and not os.environ.get('POSTGRES_URL'):
    from django.db import connection, OperationalError
    from django.core.management import call_command
    try:
        with connection.cursor() as cursor:
            # Check if auth_user table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
            if not cursor.fetchone():
                # Database is empty (new cold start), run migrations and seed
                call_command('migrate', '--noinput')
                call_command('seed_data')
    except Exception:
        pass

# Auto-run migrations on serverless cold start (Vercel)
if os.environ.get('DATABASE_URL'):
    try:
        from django.core.management import call_command
        call_command('migrate', '--noinput')
    except Exception as e:
        print(f"Auto-migrate skipped: {e}")

app = application

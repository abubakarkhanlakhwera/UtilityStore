from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib import messages
import logging
from datetime import datetime
import time

# Initialize a logger for session timeouts
logger = logging.getLogger(__name__)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware and the response callable."""
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')

            if last_activity_str:
                # Convert the string back to a datetime object
                last_activity = datetime.fromisoformat(last_activity_str)

                idle_duration = (now() - last_activity).total_seconds()
                # Check if user has been idle for longer than SESSION_COOKIE_AGE
                if idle_duration > settings.AUTO_LOGOUT.get('IDLE_TIME', 600):
                    logout(request)
                    # Redirect to login page with timeout message
                    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
            
            # Update the last activity as an ISO 8601 string
            request.session['last_activity'] = now().isoformat()

        return self.get_response(request)

    def _is_session_expired(self, request):
        """Check if the session has expired based on idle time."""
        last_activity = request.session.get('last_activity')
        if last_activity:
            idle_duration = (now() - last_activity).total_seconds()
            return idle_duration > settings.SESSION_COOKIE_AGE
        return False

    def _logout_user(self, request):
        """Logout the user and send a session timeout message."""
        logger.info(f"Logging out user {request.user} due to inactivity.")
        logout(request)
        messages.add_message(request, messages.WARNING, 'Your session has timed out due to inactivity. Please log in again.')


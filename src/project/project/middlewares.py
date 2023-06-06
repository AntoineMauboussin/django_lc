from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class LogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        action = view_func.__name__

        logger.info(f"Utilisateur: {user} - Action: {action}")

        return None

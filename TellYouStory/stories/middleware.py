
import logging

logger = logging.getLogger('middleware_logger')

class MiddlewareLogger:
    """
    Логгер приложения stories
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f'{request.method} {request.path}, {request.user}')
        response = self.get_response(request)
        return response
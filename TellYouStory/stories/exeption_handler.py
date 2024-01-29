from django.shortcuts import render
from rest_framework import status


def bad_request_handler(request, exception=None):
    """
    Обработка ошибки 400
    """
    return render(request, "400.html", status=status.HTTP_400_BAD_REQUEST)


def premission_denied_handler(request, exception=None):
    """
    Обработка ошибки 403
    """
    return render(request, "403.html", status=status.HTTP_403_FORBIDDEN)


def page_not_found_handler(request, exception=None):
    """
    Обработка ошибки 404
    """
    return render(request, "404.html", status=status.HTTP_404_NOT_FOUND)


def server_error_handler(request, exception=None):
    """
    Обработка ошибок сервера
    """
    return render(request, "500.html", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
